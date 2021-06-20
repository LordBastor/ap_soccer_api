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
            "parent_first_name",
            "parent_last_name",
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
    search_fields = ("first_name", "last_name", "id_clinic")
    list_filter = ("position", "id_clinic")

    actions = ["invite_on_trip"]
    resource_class = PlayerResource

    def invite_on_trip(modeladmin, request, queryset):
        # Grab the active trips only
        trips = Trip.objects.filter(from_date__gte=datetime.date.today())

        player_ids = [str(_id) for _id in queryset.values_list("id", flat=True)]
        response = TemplateResponse(
            request,
            "invite_on_trip.html",
            {"players": queryset, "trips": trips, "player_ids": ",".join(player_ids)},
        )
        return response


admin.site.register(Player, PlayerAdmin)
