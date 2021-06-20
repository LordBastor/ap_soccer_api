from django.urls import path

from players.views import invite_to_trip

urlpatterns = [
    path("invite_to_trip/", invite_to_trip, name="invite-to-trip"),
]

app_name = "players"
