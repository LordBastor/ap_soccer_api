from decimal import Decimal

from django.http import Http404
from django.utils import timezone
from payments.invoice_utils import generate_invoice_for_trip_invite
from payments.models import Payment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from trips.models import TripInvitation, TripTerms
from trips.serializers import (
    TripDocumentUploadSerializer,
    TripInvitationSerializer,
    TripTermSerializer,
)


class TripInvitationView(APIView):
    def get(self, request, uid):
        try:
            trip_invitation = TripInvitation.objects.get(uid=uid)
        except TripInvitation.DoesNotExist:
            raise Http404()
        serializer = TripInvitationSerializer(trip_invitation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uid):
        # TODO: Setup invoice when status is TERMS_AGREED
        try:
            trip_invitation = TripInvitation.objects.get(uid=uid)
        except TripInvitation.DoesNotExist:
            raise Http404()

        data = request.data

        create_payment = False
        amount_due = None
        amount_deposit = None

        # Let's ensure no one is pushing wrong statuses or status is being pushed back
        if "status" in data and data["status"]:
            current_status = trip_invitation.status
            future_status = data["status"]

            status_order = [
                TripInvitation.INVITE_SENT,
                TripInvitation.STARTED,
                TripInvitation.PLAYER_DATA_FILLED,
                TripInvitation.COMPANION_DATA_FILLED,
                TripInvitation.TERMS_AGREED,
                TripInvitation.INVOICE_SENT,
                TripInvitation.DEPOSIT_PAID,
                TripInvitation.PAID,
            ]

            # We should block attempts to "decrement" status
            if status_order.index(future_status) < status_order.index(current_status):
                data["status"] = current_status

            # If Companion data has been filled - let's calculate the payment
            if future_status == TripInvitation.COMPANION_DATA_FILLED:
                trip = trip_invitation.trip

                # Initial values from trip
                deposit_amount = trip.deposit_amount
                player_price = trip.player_price
                traveler_price = trip.traveler_price

                # Deposit and Amount due
                amount_due = player_price
                amount_deposit = deposit_amount

                companion_data = data["form_information"].get("companions", None)

                if companion_data:
                    if "players" in companion_data and companion_data["players"]:
                        amount_due += player_price * len(companion_data["players"])
                        amount_deposit += deposit_amount * len(
                            companion_data["players"]
                        )

                    if "companions" in companion_data and companion_data["companions"]:
                        for companion in companion_data["companions"]:
                            amount_due += traveler_price
                            amount_deposit += deposit_amount

                            if (
                                "additional_price" in companion
                                and companion["additional_price"]
                            ):
                                amount_due += Decimal(companion["additional_price"])

                create_payment = True

                data["total_amount_due"] = amount_due

            if future_status in [TripInvitation.DEPOSIT_PAID, TripInvitation.PAID]:
                return Response(
                    {
                        "error": "Don't be cheeky, you can't push these statuses manually"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = TripInvitationSerializer(trip_invitation, data=data, partial=True)

        if serializer.is_valid():
            trip_invite = serializer.save()

            # Add payment if relevant
            if create_payment:
                payment = Payment.objects.create(
                    amount_due=amount_due,
                    amount_deposit=amount_deposit,
                )
                trip_invite.payment = payment
                trip_invite.save()

            # If the terms have been agreed - let us generate the invoice
            if future_status == TripInvitation.TERMS_AGREED:
                generate_invoice_for_trip_invite(trip_invite, True)

                trip_invite.terms_accepted_on = timezone.now()
                trip_invite.status = TripInvitation.INVOICE_SENT

                trip_invite.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripTermsView(APIView):
    def get(self, request):
        # Always return the latest trips

        terms = TripTerms.objects.latest("id")

        serializer = TripTermSerializer(terms)

        return Response(serializer.data, status=status.HTTP_200_OK)


# ViewSets define the view behavior.
class TripDocumentUploadView(APIView):
    serializer_class = TripDocumentUploadSerializer

    def post(self, request, uid):
        try:
            trip_invitation = TripInvitation.objects.get(uid=uid)
        except TripInvitation.DoesNotExist:
            return Response("Trip invitation {} does not exist".format(uid))

        document = request.FILES.get("file")
        content_type = document.content_type

        allowed_content_type = [
            "application/pdf",
            "image/png",
            "image/jpg",
            "image/jpeg",
            "image/gif",
        ]

        if content_type not in allowed_content_type:
            return Response(
                "File is not a PDF or Image", status=status.HTTP_400_BAD_REQUEST
            )

        data = {"document": document, "trip_invitation": trip_invitation.pk}

        self.serializer_class(data=data)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
