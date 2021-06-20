from django.db import models

from django.db.models import Sum


class PayPalInvoice(models.Model):
    DEPOSIT = "Deposit"
    REST = "Rest"

    INVOICE_TYPE_CHOICES = (
        (DEPOSIT, DEPOSIT),
        (REST, REST),
    )

    payment = models.ForeignKey("payments.Payment", on_delete=models.PROTECT)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    invoice_number = models.CharField(max_length=255, null=True, blank=True)
    invoice_url = models.CharField(max_length=255, null=True, blank=True)
    invoice_type = models.CharField(
        max_length=30, choices=INVOICE_TYPE_CHOICES, null=True, blank=True
    )

    def __str__(self):
        return "Invoice #{} Paid: ${}/${}".format(
            self.invoice_number, float(self.amount_paid), float(self.amount_due)
        )


class Payment(models.Model):
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_deposit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        total_amount_paid = self.paypalinvoice_set.aggregate(Sum("amount_paid"))[
            "amount_paid__sum"
        ]
        if not total_amount_paid:
            total_amount_paid = 0
        return "Paid/Due: {}$/{}$".format(
            float(total_amount_paid), float(self.amount_due)
        )
