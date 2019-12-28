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


class TripCompanion(models.Model):
    package = models.ForeignKey("trips.Package", on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)

    def __str__(self):
        return "{} - {}".format(self.name, self.role)


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
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=INVITE_SENT
    )
    player = models.ForeignKey("players.Player", on_delete=models.PROTECT)
    trip = models.ForeignKey("trips.Trip", on_delete=models.PROTECT)
    payment = models.ForeignKey(
        "payments.Payment", on_delete=models.PROTECT, blank=True, null=True
    )

    # If applicable - we can add more players to an invite
    additional_players = models.ManyToManyField(
        "players.Player", related_name="additional_players", blank=True
    )
    companions = models.ManyToManyField("trips.TripCompanion", blank=True)
    total_amount_due = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )

    # TODO: Send invitation email post_save
    # TODO: Calculate total amount post_save
    # TODO: Check if email bounced on send
    # TODO: Add email recieved - tracking pixel

    def __str__(self):
        return "Trip: {} for player {} with status {}".format(
            self.trip, self.player, self.status
        )
