from django.contrib import admin
from django.core.exceptions import ValidationError

from django.forms import ModelForm

from .models import Package, Trip, TripInvitation, TripCompanion


class PackageAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("name", "price")


admin.site.register(Package, PackageAdmin)


class TripCompanionAdmin(admin.ModelAdmin):
    pass


admin.site.register(TripCompanion, TripCompanionAdmin)


class TripAdminForm(ModelForm):
    def clean_live(self):
        # Publishing a Trip is only possible if it has from-to dates
        if self.cleaned_data["live"] and not (
            self.cleaned_data["from_date"] or self.cleaned_data["to_date"]
        ):
            raise ValidationError(
                "Trip has to have from_date and to_date defined in order to go live"
            )
        return self.cleaned_data["live"]


class TripAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "from_date",
        "to_date",
        "live",
        "player_price",
        "traveler_price",
    )
    search_fields = ("name",)
    list_filter = ("live",)
    form = TripAdminForm


admin.site.register(Trip, TripAdmin)


class PlayerInline(admin.TabularInline):
    model = TripInvitation.additional_players.through
    fields = ("player_name", "player_position")
    readonly_fields = ("player_name", "player_position")
    extra = 0

    def has_add_permission(self, request):
        return False

    def player_name(self, instance):
        if instance:
            return "{} {}".format(instance.player.first_name, instance.player.last_name)

    player_name.short_description = "Player Name"

    def player_position(self, instance):
        if instance:
            return instance.player.position

    player_position.short_description = "Player Position"


class CompanionInline(admin.TabularInline):
    model = TripInvitation.companions.through
    fields = ("companion_name", "companion_role")
    readonly_fields = ("companion_name", "companion_role")
    can_delete = False
    extra = 0

    def has_add_permission(self, request):
        return False

    def companion_name(self, instance):
        if instance:
            return instance.tripcompanion.name

    companion_name.short_description = "Companion Name"

    def companion_role(self, instance):
        if instance:
            return instance.tripcompanion.role

    companion_role.short_description = "Companion Role"


class TripInvitationAdmin(admin.ModelAdmin):
    list_display = ("player", "trip", "status", "get_paid_total")
    readonly_fields = ("status", "total_amount_due", "payment")
    list_filter = ("status",)
    exclude = ("additional_players", "companions")
    can_delete = False
    can_add_related = False

    inlines = (CompanionInline, PlayerInline)

    def get_paid_total(self, obj):
        if obj.payment:
            return "${} out of ${}".format(
                int(obj.payment.amount_paid), int(obj.payment.amount_due)
            )
        else:
            return "Not submitted"

    get_paid_total.short_description = "Current Amount Paid"


admin.site.register(TripInvitation, TripInvitationAdmin)
