import uuid
from datetime import timedelta
from decimal import Decimal

from app.model_utils import BaseModel
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


class TripTerms(BaseModel):
    terms_and_conditions = models.TextField()

    class Meta:
        verbose_name_plural = "trip terms"

    def __str__(self):
        return "Terms Created On: {}".format(self.created_date)


class TripCustomTerm(BaseModel):
    terms_name = models.CharField(max_length=30)
    custom_terms = models.TextField()

    def __str__(self):
        return self.terms_name

    class Meta:
        verbose_name_plural = "Trip Custom Terms"


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
    deposit_files = models.ManyToManyField(
        "trips.TripDocument", blank=True, related_name="deposit_files"
    )
    additional_terms = models.ForeignKey(
        "trips.TripCustomTerm",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        help_text="Selected additional terms and conditions will appear on T&C step",
    )

    def __str__(self):
        return "{} from {} to {}".format(self.name, self.from_date, self.to_date)


class TripDocument(BaseModel):
    document = models.FileField(upload_to="documents/")

    def __str__(self):
        return self.document.url


def get_trip_invitation_file_path(instance, filename):
    return "trip_{}/{}".format(str(instance.trip_invitation.uid), filename)


class TripInvitationFile(BaseModel):
    document = models.FileField(upload_to=get_trip_invitation_file_path)
    trip_invitation = models.ForeignKey(
        "trips.TripInvitation", on_delete=models.PROTECT
    )

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
    additional_terms = models.ForeignKey(
        "trips.TripCustomTerm", on_delete=models.PROTECT, blank=True, null=True
    )
    terms_signature = models.ImageField(upload_to="images/", blank=True, null=True)
    terms_names = models.CharField(max_length=30, blank=True, null=True)
    terms_accepted_on = models.DateTimeField(null=True)

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

    @property
    def accepted_terms(self):
        if self.terms:
            return self.terms.id
        return "Terms not accepted yet"
