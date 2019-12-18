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
    # player = models.ForeignKey("players.Player", on_delete=models.PROTECT)
    # trip = models.ForeignKey("trips.Trip", on_delete=models.PROTECT)
    # uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # payment =
    # status =
    pass

    # TODO: Send invitation email post_save
