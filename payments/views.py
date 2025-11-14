# mpesa/views.py
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_daraja.mpesa.core import MpesaClient
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.db.models import Q

from .models import MpesaTransaction
from .serializers import MpesaTransactionSerializer
from .permissions import IsTreasurer

# -----------------API TO INITIATE PAYMENT-------------------
class InitiatePaymentAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MpesaTransactionSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            phone_number = validated_data.get('phone_number')
            amount = validated_data.get('amount')
            purpose_choice = validated_data.get('purpose')
            other_purpose_details = validated_data.get('other_purpose_details')

            final_purpose_text = other_purpose_details if purpose_choice == 'Other' else purpose_choice

            # Normalize phone number
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]
            elif phone_number.startswith('+'):
                phone_number = phone_number[1:]

            formatted_purpose = final_purpose_text.upper().replace(' ', '')
            account_reference = f"441211#{formatted_purpose}"
            transaction_desc = f"#{formatted_purpose}"

            cl = MpesaClient()

            try:
                response = cl.stk_push(
                    phone_number=phone_number,
                    amount=int(amount),
                    account_reference=account_reference,
                    transaction_desc=transaction_desc,
                    callback_url='https://churchmedia.kahawawendanisda.org/api/v1/mpesa/callback'
                )

                # Ensure checkout_request_id exists
                checkout_request_id = getattr(response, 'checkout_request_id', None)
                if not checkout_request_id:
                    return Response(
                        {"error": "MPESA did not return a CheckoutRequestID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Prevent duplicates
                transaction, created = MpesaTransaction.objects.get_or_create(
                    checkout_request_id=checkout_request_id,
                    defaults={
                        "name": validated_data.get("name"),
                        "phone_number": phone_number,
                        "amount": amount,
                        "purpose": purpose_choice,
                        "other_purpose_details": other_purpose_details,
                    }
                )

                if not created:
                    return Response(
                        {"error": "Transaction already exists"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                return Response(
                    {
                        "message": "STK push initiated successfully. Please enter your PIN.",
                        "data": MpesaTransactionSerializer(transaction).data
                    },
                    status=status.HTTP_201_CREATED
                )

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- M-Pesa Callback View ---
# This view is a webhook and should not be a DRF view.
# It needs to be accessible without authentication/tokens.
@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        stk_callback = data.get('Body', {}).get('stkCallback', {})

        # Log for debugging
        print("--- M-PESA CALLBACK RECEIVED ---")
        print(stk_callback)

        result_code = stk_callback.get('ResultCode')
        checkout_request_id = stk_callback.get('CheckoutRequestID')

        if not checkout_request_id:
            return Response(
                {"error": "Missing CheckoutRequestID in callback"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get transaction or return 404
        try:
            transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
        except MpesaTransaction.DoesNotExist:
            return Response(
                {"error": "Transaction with this CheckoutRequestID not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent double processing
        if transaction.status in ['SUCCESS', 'FAILED']:
            return Response(
                {"status": f"Transaction already processed with status: {transaction.status}"},
                status=status.HTTP_200_OK
            )

        if result_code == 0:
            transaction.status = 'SUCCESS'
            callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])

            for item in callback_metadata:
                if item.get('Name') == 'MpesaReceiptNumber':
                    transaction.mpesa_receipt_number = item.get('Value')
                elif item.get('Name') == 'TransactionDate':
                    date_str = str(item.get('Value'))
                    try:
                        transaction.transaction_date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
                    except ValueError:
                        print(f"Warning: Could not parse transaction date: {date_str}")

            transaction.save()
        else:
            transaction.status = 'FAILED'
            transaction.save()

        return Response({"status": "Callback processed successfully"}, status=status.HTTP_200_OK)
    

# -----------View All Transaction Made-----------

class MpesaTransactionsAPIView(ListAPIView):
    """
    This view provides a list of all Mpesa transactions.
    Only admin users can access this view.
    """
    serializer_class = MpesaTransactionSerializer
    permission_classes = [IsTreasurer]

    def get_queryset(self):
        queryset = MpesaTransaction.objects.all().order_by('-id')

        # ----- GET PARAMETERS -----
        status = self.request.query_params.get('status')
        purpose = self.request.query_params.get('purpose')
        search = self.request.query_params.get('search')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # ----------FILTER:STATUS-------
        if status and status != "all":
            queryset = queryset.filter(status__iexact=status)

        # ----- FILTER: Purpose -----
        if purpose and purpose != "all":
            queryset = queryset.filter(purpose__iexact=purpose)

        # ----- SEARCH (name, phone, email, receipt) -----
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(phone_number__icontains=search)
                | Q(email__icontains=search)
                | Q(mpesa_receipt_number__icontains=search)
            )
        
        # ----- DATE RANGE -----
        if start_date:
            queryset = queryset.filter(transaction_date__date__gte=start_date)


        if end_date:
            queryset = queryset.filter(transaction_date__date__lte=end_date)
        
        return queryset


