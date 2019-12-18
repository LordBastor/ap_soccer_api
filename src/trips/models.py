from django.db import models

from decimal import Decimal

import uuid


class Package(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{} - ${}".format(self.name, self.price)


class Trip(models.Model):
    name = models.CharField(max_length=255, blank=False)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    live = models.BooleanField(default=False)
    deposit_amount = models.DecimalField(
        max_digits=7, decimal_places=2, default=Decimal(500.00)
    )
    player_price = models.DecimalField(max_digits=7, decimal_places=2)
    traveler_price = models.DecimalField(max_digits=7, decimal_places=2)
    package_options = models.ManyToManyField(Package)

    def __str__(self):
        return "{} from {} to {}".format(self.name, self.from_date, self.to_date)


class TripInvitation(models.Model):
    INVITE_SENT = "Invite Sent"
    INVOICE_SENT = "Invoice Sent"
    STARTED = "Started"
    DEPOSIT_PAID = "Deposit Paid"
    PAID = "Paid"

    STATUS_CHOICES = (
        (INVITE_SENT, INVITE_SENT),
        (INVOICE_SENT, INVOICE_SENT),
        (STARTED, STARTED),
        (DEPOSIT_PAID, DEPOSIT_PAID),
        (PAID, PAID),
    )

    # Relations and status
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    player = models.ForeignKey("players.Player", on_delete=models.PROTECT)
    trip = models.ForeignKey("trips.Trip", on_delete=models.PROTECT)
    payment = models.ForeignKey("payments.Payment", on_delete=models.PROTECT)

    # Information
    # additional_players
    # additional_travelers
    # total amount_due
    # package choices

    # TODO: Send invitation email post_save
