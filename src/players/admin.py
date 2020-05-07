import datetime

from django.contrib import admin
from django.template.response import TemplateResponse

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from players.models import Player

from trips.models import Trip


class PlayerResource(resources.ModelResource):
    class Meta:
        model = Player
        fields = (
            "first_name",
            "last_name",
            "parent_name",
            "position",
            "gender",
            "address",
            "date_of_birth",
            "city",
            "state",
            "country",
            "zip_code",
            "phone",
            "email",
            "medical_conditions",
            "emergency_contact",
            "id_clinic",
        )


class PlayerAdmin(ImportExportModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "position",
        "email",
        "address",
        "date_of_birth",
        "city",
        "state",
        "id_clinic",
    )
    search_fields = ("name",)
    list_filter = ("position", "id_clinic")

    actions = ["invite_on_trip"]
    resource_class = PlayerResource

    def invite_on_trip(modeladmin, request, queryset):
        # Grab the active trips only
        trips = Trip.objects.filter(from_date__gte=datetime.date.today())
        response = TemplateResponse(
            request, "invite_on_trip.html", {"players": queryset, "trips": trips},
        )
        return response


admin.site.register(Player, PlayerAdmin)
