from django.contrib import admin
from django.template.response import TemplateResponse

from .models import Payment, PayPalInvoice


class PayPalInvoiceInline(admin.StackedInline):
    model = PayPalInvoice
    can_delete = False
    extra = 0
    max_num = 0
    readonly_fields = (
        "invoice_number",
        "invoice_url",
        "amount_due",
        "amount_paid",
        "invoice_type",
    )
    list_display = (
        "payment",
        "amount_paid",
        "invoice_number",
        "invoice_url",
        "invoice_type",
    )


class PayPalInvoiceAdmin(admin.ModelAdmin):
    model = PayPalInvoice
    readonly_fields = (
        "invoice_number",
        "invoice_url",
    )
    list_display = (
        "amount_paid",
        "amount_due",
        "invoice_number",
        "invoice_url",
        "invoice_type",
    )
    actions = ["record_payment"]

    search_fields = (
        "invoice_number",
        "invoice_url",
    )

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


admin.site.register(PayPalInvoice, PayPalInvoiceAdmin)


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    readonly_fields = (
        "amount_due",
        "amount_deposit",
    )
    list_display = (
        "amount_due",
        "amount_deposit",
    )

    inlines = [
        PayPalInvoiceInline,
    ]


admin.site.register(Payment, PaymentAdmin)
