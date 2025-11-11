from django.urls import path
from .views import InitiatePaymentAPIView, MpesaCallbackView

urlpatterns = [
    # API endpoint to start the payment process
    path('initiate-payment/', InitiatePaymentAPIView.as_view(), name='initiate_payment_api'),
    
    # Webhook endpoint for Safaricom to send the transaction result
    path('callback', MpesaCallbackView.as_view(), name='mpesa_callback_api'),
]