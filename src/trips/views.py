from django.http import Http404
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from trips.models import TripInvitation, TripTerms
from trips.serializers import TripInvitationSerializer, TripTermSerializer


class TripInvitationView(APIView):
    def get(self, request, uid):
        try:
            trip_invitation = TripInvitation.objects.get(uid=uid)
        except TripInvitation.DoesNotExist:
            raise Http404()
        serializer = TripInvitationSerializer(trip_invitation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uid):
        # TODO: Calculate total amount when step is PLAYER_DATA_FILLED
        # TODO: Setup invoice when status is TERMS_AGREED
        try:
            trip_invitation = TripInvitation.objects.get(uid=uid)
        except TripInvitation.DoesNotExist:
            raise Http404()

        data = request.data

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

            if future_status in [TripInvitation.DEPOSIT_PAID, TripInvitation.PAID]:
                return Response(
                    {
                        "error": "Don't be cheeky, you can't push these statuses manually"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = TripInvitationSerializer(trip_invitation, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripTermsView(APIView):
    def get(self, request):
        # Always return the latest trips

        terms = TripTerms.objects.latest("id")

        serializer = TripTermSerializer(terms)

        return Response(serializer.data, status=status.HTTP_200_OK)
