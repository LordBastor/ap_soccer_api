from django.db import models


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
        return "adsaInvoice #{} Paid: ${}/${}".format(
            self.invoice_number, int(self.amount_paid), int(self.amount_due)
        )


class Payment(models.Model):
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_deposit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return "Paid/Due: {}$/{}$".format(int(self.amount_due), int(self.amount_due))
