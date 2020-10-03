from django.db import models


class Payment(models.Model):
    invoice_number = models.CharField(max_length=255, null=True, blank=True)
    invoice_url = models.CharField(max_length=255, null=True, blank=True)
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    amount_deposit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return "Invoice: {} Paid/Due: {}$/{}$".format(
            self.invoice_number, int(self.amount_paid), int(self.amount_due)
        )
