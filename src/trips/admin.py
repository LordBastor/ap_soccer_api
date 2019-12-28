from django.contrib import admin
from django.core.exceptions import ValidationError

from django.forms import ModelForm

from .models import Package, Trip, TripInvitation


class PackageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Package, PackageAdmin)


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


class TripInvitationAdmin(admin.ModelAdmin):
    list_display = ("player", "trip", "status", "get_paid_total")
    readonly_fields = ("status", "total_amount_due", "payment")
    list_filter = ("status",)

    def get_paid_total(self, obj):
        if obj.payment:
            return "${} out of ${}".format(
                int(obj.payment.amount_paid), int(obj.payment.amount_due)
            )
        else:
            return "Not submitted"


admin.site.register(TripInvitation, TripInvitationAdmin)
