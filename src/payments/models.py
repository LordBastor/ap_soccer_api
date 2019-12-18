from django.db import models


class Payment(models.Model):
    invoice_number = models.CharField(max_length=255)
    invoice_url = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.invoice_number
