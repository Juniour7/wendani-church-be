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
from .coopbank import stk_push_request

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
            return Response(serializer.errors, status=400)

        validated = serializer.validated_data
        phone = validated["phone_number"]
        purposes = validated["purposes"]

        # Normalize phone
        if phone.startswith("0"):
            phone = "254" + phone[1:]
        elif phone.startswith("+"):
            phone = phone[1:]

        # ----- Build Co-op OtherDetails -----
        other_details = []
        total_amount = 0

        for p in purposes:
            purpose_name = p["purpose"]
            amount = int(p["amount"])
            total_amount += amount

            # Custom field support
            if purpose_name == "Other" and p.get("other_purpose_details"):
                key = p["other_purpose_details"]
            else:
                key = purpose_name

            other_details.append({"Name": key, "Value": str(amount)})

        # Tag for narration
        if len(purposes) == 1:
            tag = purposes[0]["purpose"].replace(" ", "")
        else:
            tag = "MULTI"

        reference = f"{tag}"

        # ----- Save to DB -----
        transaction = serializer.save(
            checkout_request_id=reference,
            total_amount=total_amount
        )

        # ----- Call Co-op Bank -----
        try:
            response = stk_push_request(
                phone=phone,
                amount=int(total_amount),
                reference=reference,
                other_details=other_details,
                description=tag
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({
            "message": "STK Push sent. Enter PIN.",
            "checkout_request_id": reference,
            "amount": total_amount,
            "co_op_response": response,
        }, status=201)





# ------------------------ M-Pesa Callback View ------------------------
@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(APIView):
    """
    Handle Co-op Bank STK push callback
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data

        message_ref = data.get("MessageReference")
        response_code = data.get("ResponseCode")
        result = data.get("Result", {})

        if not message_ref:
            return Response({"error": "Missing MessageReference"}, status=400)

        try:
            transaction = MpesaTransaction.objects.get(checkout_request_id=message_ref)
        except MpesaTransaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

        # Avoid double processing
        if transaction.status in ["SUCCESS", "FAILED"]:
            return Response({"status": f"Transaction already processed: {transaction.status}"}, status=200)

        if response_code == "0":
            # Payment successful
            transaction.status = "SUCCESS"
            transaction.mpesa_receipt_number = result.get("MpesaReceiptNumber")
            # If Co-op returns a transaction date, parse it; else use now()
            date_str = result.get("TransactionDate")
            if date_str:
                try:
                    transaction.transaction_date = datetime.strptime(date_str, "%Y%m%d%H%M%S")
                except ValueError:
                    transaction.transaction_date = datetime.now()
            else:
                transaction.transaction_date = datetime.now()
        else:
            # Payment failed
            transaction.status = "FAILED"

        transaction.save()

        return Response({"status": "Callback processed successfully"}, status=200)




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