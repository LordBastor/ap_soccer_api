from django.contrib import admin

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


admin.site.register(Payment, PaymentAdmin)
