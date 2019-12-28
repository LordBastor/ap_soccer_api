from django.contrib import admin

from .models import Player


class PlayerAdmin(admin.ModelAdmin):
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


admin.site.register(Player, PlayerAdmin)
