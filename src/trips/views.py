from django.http import Http404
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from trips.models import TripInvitation
from trips.serializers import TripInvitationSerializer


class TripInvitationView(APIView):
    def get(self, request, uid):
        try:
            trip_invitation = TripInvitation.objects.get(uid=uid)
        except TripInvitation.DoesNotExist:
            raise Http404()
        serializer = TripInvitationSerializer(trip_invitation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uid):
        try:
            trip_invitation = TripInvitation.objects.get(uid=uid)
        except TripInvitation.DoesNotExist:
            raise Http404()

        data = request.data

        serializer = TripInvitationSerializer(trip_invitation, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
