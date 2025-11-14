from rest_framework import serializers
from .models import MpesaTransaction

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = [
            'id', 'name', 'phone_number', 'email', 'amount', 'purpose', 
            'other_purpose_details', 'status', 'mpesa_receipt_number', 'checkout_request_id', 'transaction_date'
        ]
        read_only_fields = ['id', 'status', 'mpesa_receipt_number', 'transaction_date', 'checkout_request_id']

    
    def validate(self, data):
        """
        Custom validation to ensure 'other_purpose_details' is provided if purpose is 'Other'.
        """
        if data.get('purpose') == 'Other' and not data.get('other_purpose_details'):
            raise serializers.ValidationError({
                "other_purpose_details": "This field is required when the purpose is 'Other'."
            })
        
        # Ensure 'other_purpose_details' is ignored if purpose is not 'Other'
        if data.get('purpose') != 'Other':
            data['other_purpose_details'] = None

        return data
