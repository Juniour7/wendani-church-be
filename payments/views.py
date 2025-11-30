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
from django.db.models import Q

from .models import MpesaTransaction, MpesaPurpose
from .serializers import MpesaTransactionSerializer
from .permissions import IsTreasurer


# ----------------- API TO INITIATE PAYMENT -------------------
class InitiatePaymentAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MpesaTransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        phone_number = validated.get("phone_number")
        purposes = validated.get("purposes")   # list of {"purpose", "amount", ...}

        # Normalize phone number
        if phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]
        elif phone_number.startswith("+"):
            phone_number = phone_number[1:]

        # Determine STK label (#TITHE, #MULTI, etc.)
        if len(purposes) == 1:
            tag = purposes[0]["purpose"].upper().replace(" ", "")
        else:
            tag = "MULTI"

        account_reference = f"441211#{tag}"
        transaction_desc = f"#{tag}"

        # SUM all amounts
        total_amount = sum([p["amount"] for p in purposes])

        cl = MpesaClient()

        try:
            response = cl.stk_push(
                phone_number=phone_number,
                amount=int(total_amount),
                account_reference=account_reference,
                transaction_desc=transaction_desc,
                callback_url='https://churchmedia.kahawawendanisda.org/api/v1/mpesa/callback'
            )

            checkout_request_id = getattr(response, "checkout_request_id", None)
            if not checkout_request_id:
                return Response(
                    {"error": "MPESA did not return a CheckoutRequestID"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save parent + child purposes
            transaction = serializer.save(
                checkout_request_id=checkout_request_id,
                total_amount=total_amount
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



# ------------------------ M-Pesa Callback View ------------------------
@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        stk_callback = data.get('Body', {}).get('stkCallback', {})

        result_code = stk_callback.get('ResultCode')
        checkout_request_id = stk_callback.get('CheckoutRequestID')

        if not checkout_request_id:
            return Response(
                {"error": "Missing CheckoutRequestID in callback"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
        except MpesaTransaction.DoesNotExist:
            return Response(
                {"error": "Transaction with this CheckoutRequestID not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Avoid double processing
        if transaction.status in ["SUCCESS", "FAILED"]:
            return Response(
                {"status": f"Transaction already processed: {transaction.status}"},
                status=status.HTTP_200_OK
            )

        # SUCCESS
        if result_code == 0:
            transaction.status = "SUCCESS"
            callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])

            for item in callback_metadata:
                if item.get("Name") == "MpesaReceiptNumber":
                    transaction.mpesa_receipt_number = item.get("Value")
                elif item.get("Name") == "TransactionDate":
                    date_str = str(item.get("Value"))
                    try:
                        transaction.transaction_date = datetime.strptime(date_str, "%Y%m%d%H%M%S")
                    except ValueError:
                        pass

            transaction.save()

        # FAILURE
        else:
            transaction.status = "FAILED"
            transaction.save()

        return Response({"status": "Callback processed successfully"}, status=status.HTTP_200_OK)



# ----------------- View All Transactions -------------------
class MpesaTransactionsAPIView(ListAPIView):
    serializer_class = MpesaTransactionSerializer
    permission_classes = [IsTreasurer]

    def get_queryset(self):
        queryset = MpesaTransaction.objects.all().order_by("-id")

        status_q = self.request.query_params.get("status")
        purpose = self.request.query_params.get("purpose")
        search = self.request.query_params.get("search")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        # Filter by status
        if status_q and status_q != "all":
            queryset = queryset.filter(status__iexact=status_q)

        # Filter by specific purpose inside children
        if purpose and purpose != "all":
            queryset = queryset.filter(purposes__purpose__iexact=purpose)

        # Search
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(phone_number__icontains=search)
                | Q(email__icontains=search)
                | Q(mpesa_receipt_number__icontains=search)
            ).distinct()

        # Date filters
        if start_date:
            queryset = queryset.filter(transaction_date__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(transaction_date__date__lte=end_date)

        return queryset



# ----------------- Check Transaction Status -------------------
class TransactionStatusAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        checkout_request_id = request.query_params.get("checkout_request_id")

        if not checkout_request_id:
            return Response({"error": "checkout_request_id is required"}, status=400)

        try:
            transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
        except MpesaTransaction.DoesNotExist:
            return Response({"status": "not_found"}, status=404)

        purposes = [
            {
                "purpose": p.purpose,
                "amount": p.amount,
                "other_purpose_details": p.other_purpose_details,
            }
            for p in transaction.purposes.all()
        ]

        tag = "#MULTI" if len(purposes) > 1 else f"#{purposes[0]['purpose'].upper()}"

        return Response({
            "status": transaction.status,
            "mpesa_receipt_number": transaction.mpesa_receipt_number,
            "transaction_date": transaction.transaction_date,
            "total_amount": transaction.total_amount,
            "purposes": purposes,
            "tag": tag
        })
