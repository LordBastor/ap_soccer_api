from django.contrib import admin, forms

from .models import Package, Trip


class PackageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Package, PackageAdmin)


class TripAdminForm(forms.ModelAdmin):
    def clean_live(self):
        import ipdb

        ipdb.set_trace()


class TripAdmin(admin.ModelAdmin):
    form = TripAdminForm


admin.site.register(Trip, TripAdmin)
