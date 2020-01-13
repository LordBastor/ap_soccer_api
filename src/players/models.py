from django.db import models


class Player(models.Model):
    GOALKEEPER = "Goalkeeper"
    DEFENSE = "Defense"
    MIDFIELD = "Midfield"
    FORWARD = "Forward"
    POSITION_CHOICES = (
        (GOALKEEPER, "Goalkeeper"),
        (DEFENSE, "Defense"),
        (MIDFIELD, "Midfield"),
        (FORWARD, "Forward"),
    )

    MALE = "Male"
    FEMALE = "Female"
    GENDER_CHOICES = ((MALE, "Male"), (FEMALE, "Female"))

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    parent_name = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(
        max_length=10, choices=POSITION_CHOICES, null=True, blank=True
    )
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, null=True, blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(
        max_length=255, default="United States", null=True, blank=True
    )
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255)
    medical_conditions = models.TextField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=255, null=True, blank=True)
    id_clinic = models.CharField(max_length=255, null=True, blank=True)

    # TODO: Setup player CSV ingestion

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.last_name, self.position)
