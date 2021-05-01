from rest_framework import serializers

from payments.models import Payment, PayPalInvoice


class PayPalInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPalInvoice
        fields = [
            "amount_paid",
            "amount_due",
            "invoice_number",
            "invoice_url",
            "invoice_type",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    invoices = PayPalInvoiceSerializer(source="paypalinvoice_set", many=True)

    class Meta:
        model = Payment
        fields = [
            "amount_due",
            "amount_deposit",
            "invoices",
        ]
