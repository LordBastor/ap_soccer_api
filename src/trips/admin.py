from django.contrib import admin
from django.core.exceptions import ValidationError

from django.forms import ModelForm

from .models import (
    Package,
    Trip,
    TripInvitation,
    TripCompanion,
    TripDocument,
    TripTerms,
)


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
        "terms",
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


class TripTermsAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id=None, form_url="", extra_context=None):
        # use extra_context to disable the other save (and/or delete) buttons
        extra_context = dict(
            show_save=False, show_save_and_continue=False, show_delete=False
        )
        # get a reference to the original has_add_permission method
        has_add_permission = self.has_add_permission
        # monkey patch: temporarily override has_add_permission so it returns False
        self.has_add_permission = lambda __: False
        # get the TemplateResponse from super (python 3)
        template_response = super().change_view(
            request, object_id, form_url, extra_context
        )
        # restore the original has_add_permission (otherwise we cannot add anymore)
        self.has_add_permission = has_add_permission
        # return the result
        return template_response


admin.site.register(TripTerms, TripTermsAdmin)
