from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from players.serializers import PlayerSerializer
from payments.serializer import PaymentSerializer

from trips.models import TripInvitation, Trip, Package, TripTerms


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
    player = PlayerSerializer()
    trip = TripSerializer()
    payment = PaymentSerializer()
    terms_signature = Base64ImageField()

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
            "terms",
            "terms_signature",
            "is_valid",
            "invoice_link",
        ]

        read_only_fields = [
            "uid",
            "player",
            "trip",
            "payment",
            "total_amount_due",
            "is_valid",
            "invoice_link",
        ]


class TripTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripTerms
        fields = "__all__"
