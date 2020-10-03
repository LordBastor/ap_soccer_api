from django.urls import path

from trips.views import TripInvitationView, TripTermsView

urlpatterns = [
    path(
        "invitation/<uuid:uid>",
        TripInvitationView.as_view(),
        name="trip_invitation_view",
    ),
    path("terms", TripTermsView.as_view(), name="trip_terms_view",),
]

app_name = "trips"
