from django.contrib import admin
from django.core.exceptions import ValidationError

from django.forms import ModelForm

from .models import Package, Trip, TripInvitation, TripCompanion, TripDocument


admin.site.register(TripDocument)
admin.site.register(TripCompanion)


class PackageAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("name", "price")


admin.site.register(Package, PackageAdmin)


class TripDocumentInline(admin.TabularInline):
    model = Trip.email_files.through


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
        "created_date",
    )
    search_fields = ("name",)
    list_filter = ("live",)
    form = TripAdminForm
    inlines = (TripDocumentInline,)


admin.site.register(Trip, TripAdmin)


class TripInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "trip",
        "status",
        "get_paid_total",
        "created_date",
        "form_information",
        "uid",
    )
    readonly_fields = (
        "uid",
        "status",
        "total_amount_due",
        "payment",
        "form_information",
    )
    list_filter = ("status",)
    can_delete = False
    can_add_related = False

    def get_paid_total(self, obj):
        if obj.payment:
            return "${} out of ${}".format(
                int(obj.payment.amount_paid), int(obj.payment.amount_due)
            )
        else:
            return "Not submitted"

    get_paid_total.short_description = "Current Amount Paid"


admin.site.register(TripInvitation, TripInvitationAdmin)
