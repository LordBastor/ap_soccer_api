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

    parent_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default="United States")
    zip_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    medical_conditions = models.TextField()
    emergency_contact = models.CharField(max_length=255)

    # TODO: Add clinic field to player model
    # TODO: Setup player CSV ingestion

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.position
