from django.urls import path

from trips.views import TripInvitationView

urlpatterns = [
    path(
        "invitation/<uuid:uid>",
        TripInvitationView.as_view(),
        name="trip_invitation_view",
    ),
]

app_name = "trips"
