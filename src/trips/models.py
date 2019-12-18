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
        from_date_str = None
        if self.from_date:
            from_date_str = self.from_date.date()

        to_date_str = None
        if self.to_date:
            to_date_str = self.to_date.date()

        return "{} from {} to {}".format(self.name, from_date_str, to_date_str)


class TripInvitation(models.Model):
    pass
