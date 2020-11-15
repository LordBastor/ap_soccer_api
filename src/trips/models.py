from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

from decimal import Decimal

from datetime import timedelta

from ckeditor.fields import RichTextField

from app.model_utils import BaseModel

import uuid


class TripTerms(BaseModel):
    terms_and_conditions = models.TextField()

    class Meta:
        verbose_name_plural = "trip terms"

    def __str__(self):
        return "Terms Created On: {}".format(self.created_date)


class Package(BaseModel):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{} - ${}".format(self.name, self.price)


class Trip(BaseModel):
    name = models.CharField(max_length=255, blank=False)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    live = models.BooleanField(default=False)
    deposit_amount = models.DecimalField(
        max_digits=7, decimal_places=2, default=Decimal(500.00)
    )
    player_price = models.DecimalField(max_digits=7, decimal_places=2)
    traveler_price = models.DecimalField(max_digits=7, decimal_places=2)
    package_options = models.ManyToManyField("trips.Package")
    email_template = RichTextField(blank=True, null=True)
    email_files = models.ManyToManyField("trips.TripDocument", blank=True)

    def __str__(self):
        return "{} from {} to {}".format(self.name, self.from_date, self.to_date)


class TripDocument(BaseModel):
    document = models.FileField(upload_to="documents/")

    def __str__(self):
        return self.document.url


class TripInvitation(BaseModel):
    INVITE_SENT = "Invite Sent"
    STARTED = "Started"
    PLAYER_DATA_FILLED = "Player Data Filled"
    COMPANION_DATA_FILLED = "Companion Data Filled"
    TERMS_AGREED = "Terms Agreed"
    INVOICE_SENT = "Invoice Sent"
    DEPOSIT_PAID = "Deposit Paid"
    PAID = "Paid"

    STATUS_CHOICES = (
        (INVITE_SENT, INVITE_SENT),
        (STARTED, STARTED),
        (PLAYER_DATA_FILLED, PLAYER_DATA_FILLED),
        (COMPANION_DATA_FILLED, COMPANION_DATA_FILLED),
        (TERMS_AGREED, TERMS_AGREED),
        (INVOICE_SENT, INVOICE_SENT),
        (DEPOSIT_PAID, DEPOSIT_PAID),
        (PAID, PAID),
    )

    # Relations and status
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default=INVITE_SENT
    )
    player = models.ForeignKey("players.Player", on_delete=models.PROTECT)
    trip = models.ForeignKey("trips.Trip", on_delete=models.PROTECT)
    payment = models.ForeignKey(
        "payments.Payment", on_delete=models.PROTECT, blank=True, null=True
    )

    total_amount_due = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )

    form_information = JSONField(default=dict)

    terms = models.ForeignKey(
        "trips.TripTerms", on_delete=models.PROTECT, blank=True, null=True
    )
    terms_signature = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return "Trip: {} for player {} with status {}".format(
            self.trip, self.player, self.status
        )

    @property
    def is_valid(self):
        return self.created_date + timedelta(days=10) < timezone.now()

    @property
    def invoice_link(self):
        if self.payment and self.payment.invoice_url:
            return self.payment.invoice_url
        return "Not submitted"
