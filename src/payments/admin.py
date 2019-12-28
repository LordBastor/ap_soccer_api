from django.contrib import admin

from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = (
        "invoice_number",
        "invoice_url",
        "amount_paid",
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
