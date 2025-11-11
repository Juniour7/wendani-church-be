# mpesa/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django_daraja.mpesa.core import MpesaClient
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import MpesaTransaction
from .serializers import MpesaTransactionSerializer

# -----------------API TO INITIATE PAYMENT-------------------
class InitiatePaymentAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        # Use the serializer to validate incoming data
        # Note: We are not saving the serializer directly yet. 
        # First, we trigger the STK push.
        serializer = MpesaTransactionSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            phone_number = validated_data.get('phone_number')
            amount = validated_data.get('amount')
            purpose_choice = validated_data.get('purpose')
            other_purpose_details = validated_data.get('other_purpose_details')

            # Determine the final purpose text
            final_purpose_text = other_purpose_details if purpose_choice == 'Other' else purpose_choice

            # Format the phone number (e.g., to 254...)
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]
            elif phone_number.startswith('+'):
                phone_number = phone_number[1:]

            account_reference = f"CHURCH-{purpose_choice.upper()}"
            transaction_desc = f"Contribution for {final_purpose_text}"

            cl = MpesaClient()
            try:
                response = cl.stk_push(
                    phone_number=phone_number,
                    amount=int(amount), # Amount should be an integer
                    account_reference=account_reference,
                    transaction_desc=transaction_desc,
                    callback_url='https://agreeable-hermitical-annamaria.ngrok-free.dev/api/v1/mpesa/callback' # IMPORTANT: Update this URL
                )

                # If STK push is successful, save the transaction with the CheckoutRequestID
                if hasattr(response, 'checkout_request_id'):
                    serializer.save(checkout_request_id=response.checkout_request_id)
                    return Response({
                        "message": "STK push initiated successfully. Please enter your PIN.",
                        "data": serializer.data
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Failed to initiate STK push."}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- M-Pesa Callback View ---
# This view is a webhook and should not be a DRF view.
# It needs to be accessible without authentication/tokens.
@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        stk_callback = data.get('Body', {}).get('stkCallback', {})
        
        result_code = stk_callback.get('ResultCode')
        checkout_request_id = stk_callback.get('CheckoutRequestID')

        try:
            transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
        except MpesaTransaction.DoesNotExist:
            # Safaricom might retry, so it's okay if it's not found immediately.
            # You might want to log this for monitoring.
            return Response({"status": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        if result_code == 0:
            # Payment successful
            transaction.status = 'SUCCESS'
            callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            for item in callback_metadata:
                if item['Name'] == 'MpesaReceiptNumber':
                    transaction.mpesa_receipt_number = item['Value']
                elif item['Name'] == 'TransactionDate':
                    # You might need to parse this date string to a proper datetime object
                    transaction.transaction_date = item['Value'] 
            transaction.save()
        else:
            # Payment failed or was cancelled
            transaction.status = 'FAILED'
            transaction.save()
        
        # Respond to Safaricom's API
        return Response({"status": "Callback processed successfully"}, status=status.HTTP_200_OK)