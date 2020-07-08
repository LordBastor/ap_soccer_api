from rest_framework import serializers

from players.serializers import PlayerSerializer
from payments.serializer import PaymentSerializer

from trips.models import TripInvitation, Trip, Package


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            "name",
            "price",
            "description",
        ]


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            "name",
            "from_date",
            "to_date",
            "live",
            "deposit_amount",
            "player_price",
            "traveler_price",
            "package_options",
        ]

    package_options = PackageSerializer(many=True)


class TripInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripInvitation
        fields = [
            "uid",
            "status",
            "player",
            "trip",
            "payment",
            "total_amount_due",
            "form_information",
        ]

    player = PlayerSerializer()
    trip = TripSerializer()
    payment = PaymentSerializer()
