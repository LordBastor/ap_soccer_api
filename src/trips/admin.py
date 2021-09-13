from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.html import format_html
from django.urls import reverse

from .models import Package, Trip, TripDocument, TripInvitation, TripInvitationFile, TripTerms

admin.site.register(TripDocument)


class PackageAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("name", "price")


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
        "created_date",
    )
    search_fields = ("name",)
    list_filter = ("live",)
    form = TripAdminForm
    filter_horizontal = ("email_files", "deposit_files")


admin.site.register(Trip, TripAdmin)


class TripInvitationFileInline(admin.TabularInline):
    model = TripInvitationFile
    show_change_link = False
    extra = 0


class TripInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "trip",
        "status",
        "created_date",
        "form_information",
        "uid",
    )
    readonly_fields = (
        "uid",
        "status",
        "total_amount_due",
        "invoice_link",
        "payment",
        "form_information",
        "terms_accepted_on",
        "accepted_terms",
    )
    exclude = ("terms",)
    list_filter = (
        "status",
        "trip__name",
    )
    can_delete = False
    can_add_related = False
    inlines = [TripInvitationFileInline]

    def invoice_link(self, obj):
        return format_html("<a href='{url}' target='blank'>{url}</a>", url=obj.invoice_link)

    def accepted_terms(self, obj):
        change_url = reverse("admin:trips_tripterms_change", args=[obj.terms.id])
        return format_html(
            '<a href="{change_url}" target="blank">{model_string}</a>'.format(
                change_url=change_url, model_string=obj.terms.__str__()
            )
        )

    accepted_terms.short_description = "Terms the user agreed to"
    invoice_link.short_description = "PayPal Invoice URL"


admin.site.register(TripInvitation, TripInvitationAdmin)


class TripTermsAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id=None, form_url="", extra_context=None):
        # use extra_context to disable the other save (and/or delete) buttons
        extra_context = dict(show_save=False, show_save_and_continue=False, show_delete=False)
        # get a reference to the original has_add_permission method
        has_add_permission = self.has_add_permission
        # monkey patch: temporarily override has_add_permission so it returns False
        self.has_add_permission = lambda __: False
        # get the TemplateResponse from super (python 3)
        template_response = super().change_view(request, object_id, form_url, extra_context)
        # restore the original has_add_permission (otherwise we cannot add anymore)
        self.has_add_permission = has_add_permission
        # return the result
        return template_response


admin.site.register(TripTerms, TripTermsAdmin)
