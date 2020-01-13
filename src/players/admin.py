from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Player


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
    list_filter = ("position",)

    resource_class = PlayerResource


admin.site.register(Player, PlayerAdmin)
