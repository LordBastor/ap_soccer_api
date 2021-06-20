from rest_framework import serializers

from players.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "first_name",
            "last_name",
            "parent_first_name",
            "parent_last_name",
            "position",
            "gender",
            "address",
            "date_of_birth",
            "city",
            "state",
            "country",
            "zip_code",
            "phone",
            "email",
            "medical_conditions",
            "emergency_contact",
            "id_clinic",
        ]
