from drf_extra_fields.fields import Base64ImageField
from payments.serializer import PaymentSerializer
from players.serializers import PlayerSerializer
from rest_framework import serializers
from trips.models import (
    Package,
    Trip,
    TripDocument,
    TripInvitation,
    TripInvitationFile,
    TripTerms,
    TripCustomTerm,
)


class TripCustomTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripCustomTerm
        fields = ["id", "terms_name", "custom_terms"]


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ["name", "price", "description"]


class TripDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripDocument
        fields = ["document"]


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
            "deposit_files",
            "additional_terms",
        ]

    package_options = PackageSerializer(many=True)
    deposit_files = TripDocumentSerializer(many=True)
    additional_terms = TripCustomTermSerializer()


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
            "terms_names",
            "terms_accepted_on",
            "additional_terms",
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


# Serializers define the API representation.
class TripDocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripInvitationFile
        fields = ["document", "trip_invitation"]

    document = serializers.FileField()
