from rest_framework import serializers
from .models import MpesaTransaction, MpesaPurpose


class MpesaPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaPurpose
        fields = ['purpose', 'amount', 'other_purpose_details']


class MpesaTransactionSerializer(serializers.ModelSerializer):
    purposes = MpesaPurposeSerializer(many=True)

    class Meta:
        model = MpesaTransaction
        fields = [
            'id', 'name', 'phone_number', 'email', 
            'status', 'mpesa_receipt_number', 'checkout_request_id',
            'transaction_date', 'total_amount', 'purposes'
        ]
        read_only_fields = ['id', 'status', 'mpesa_receipt_number', 'transaction_date', 'checkout_request_id']

    
    def create(self, validated_data):
        purposes_data = validated_data.pop("purposes")

        # Make parent
        parent = MpesaTransaction.objects.create(**validated_data)

        total = 0
        # Create line items
        for p in purposes_data:
            MpesaPurpose.objects.create(transaction=parent, **p)
            total += p["amount"]

        parent.total_amount = total
        parent.save()

        return parent
