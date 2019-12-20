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
    form = TripAdminForm


admin.site.register(Trip, TripAdmin)


class TripInvitationAdmin(admin.ModelAdmin):
    # TODO: Sort columns by trip status and allow for filtering based on status
    # Trip | Player | Invitation Status
    pass


admin.site.register(TripInvitation, TripInvitationAdmin)
