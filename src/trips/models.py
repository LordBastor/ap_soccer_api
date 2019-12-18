from django.db import models

from decimal import Decimal


class Package(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{} - ${}".format(self.name, self.price)


class Trip(models.Model):
    name = models.CharField(max_length=255, blank=False)
    from_date = models.DateTimeField(blank=True)
    to_date = models.DateTimeField(blank=True)
    live = models.BooleanField(default=False)
    deposit_amount = models.DecimalField(
        max_digits=7, decimal_places=2, default=Decimal(500.00)
    )
    player_price = models.DecimalField(max_digits=7, decimal_places=2)
    traveler_price = models.DecimalField(max_digits=7, decimal_places=2)
    package_options = models.ManyToManyField(Package)

    def __str__(self):
        return "{} from {} to {}".format(
            self.name, self.from_date.date(), self.to_date.date()
        )


class TripInvitation(models.Model):
    pass
