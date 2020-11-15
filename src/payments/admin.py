from django.contrib import admin
from django.template.response import TemplateResponse

from .models import Payment


class PaymentAdminInline(admin.StackedInline):
    model = Payment
    readonly_fields = (
        "invoice_number",
        "invoice_url",
        "amount_due",
    )
    list_display = (
        "invoice_number",
        "invoice_url",
        "amount_paid",
        "amount_due",
    )


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = (
        "invoice_number",
        "invoice_url",
        "amount_due",
    )
    list_display = (
        "invoice_number",
        "invoice_url",
        "amount_paid",
        "amount_due",
    )
    search_fields = (
        "invoice_number",
        "invoice_url",
    )
    actions = ["record_payment"]

    def record_payment(modeladmin, request, queryset):
        # PayPal Valid method options
        methods = [
            "BANK_TRANSFER",
            "CASH",
            "CHECK",
            "CREDIT_CARD",
            "DEBIT_CARD",
            "PAYPAL",
            "WIRE_TRANSFER",
            "OTHER",
        ]

        invoice_ids = [str(_id) for _id in queryset.values_list("id", flat=True)]

        response = TemplateResponse(
            request,
            "record_payment.html",
            {"methods": methods, "invoice_ids": ",".join(invoice_ids)},
        )
        return response


admin.site.register(Payment, PaymentAdmin)
