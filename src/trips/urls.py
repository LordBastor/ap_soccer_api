from django.urls import path
from trips.views import (TripDocumentUploadView, TripInvitationView,
                         TripTermsView)

urlpatterns = [
    path(
        "invitation/<uuid:uid>",
        TripInvitationView.as_view(),
        name="trip_invitation_view",
    ),
    path(
        "upload/<uuid:uid>",
        TripDocumentUploadView.as_view(),
        name="trip_upload_form",
    ),
    path(
        "terms",
        TripTermsView.as_view(),
        name="trip_terms_view",
    ),
]

app_name = "trips"
