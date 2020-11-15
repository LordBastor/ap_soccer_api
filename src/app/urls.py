from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Enables the DRF browsable API page
    path("players/", include("players.urls", namespace="players")),
    path("payments/", include("payments.urls", namespace="payments")),
    path("trips/", include("trips.urls", namespace="trip")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
