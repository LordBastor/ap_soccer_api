from rest_framework import serializers

from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "invoice_number",
            "invoice_url",
            "amount_due",
            "amount_paid",
        ]
