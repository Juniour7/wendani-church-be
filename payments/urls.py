from django.urls import path
from .views import InitiatePaymentAPIView, MpesaCallbackView, MpesaTransactionsAPIView, TransactionStatusAPIView, CoopTransactionStatusAPIView

urlpatterns = [
    # API endpoint to start the payment process
    path('initiate-payment/', InitiatePaymentAPIView.as_view(), name='initiate_payment_api'),
    
    # Webhook endpoint for Safaricom to send the transaction result
    path('callback', MpesaCallbackView.as_view(), name='mpesa_callback_api'),

    # Endpint to view all transactions that have been made
    path('transactions/', MpesaTransactionsAPIView.as_view(), name='mpesa_transaction_list'),
    path('status-check/', TransactionStatusAPIView.as_view(), name='status-check'),

    # Check / poll transaction status from Co-op Bank
    path('check-status/', CoopTransactionStatusAPIView.as_view(), name='coop-transaction-status'),
]