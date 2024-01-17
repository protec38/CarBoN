from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.db.models.query import QuerySet
from django.urls import reverse

from main.models import Location, Vehicle, Defect, Trip


@admin.display(description=_("Nombre de véhicules"))
def vehicle_count(obj: Location):
    return obj.vehicle_set.count()


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", vehicle_count]

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "starting_time", "ending_time", "starting_mileage", "ending_mileage", "driver_name"]
    list_filter = ["vehicle"]


class DefectInline(admin.TabularInline):
    model = Defect
    extra = 0
    fields = (
        "type",
        "comment",
        "creation_date",
        "solution_date",
        "reporter_name",
        "status",
    )
    readonly_fields = ["creation_date", "solution_date"]


@admin.display(description="Nombre d'anomalies ouvertes")
def open_defect_count(obj: Vehicle):
    return obj.defect_set.filter(status=Defect.DefectStatus.OPEN).count()


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "model_name",
        "status",
        "registration_number",
        open_defect_count,
    ]
    inlines = [DefectInline]
    actions = ["get_qr_code"]
    list_editable = ['status']

    @admin.action(description=_("Obtenir les QR codes"))
    def get_qr_code(self, request: HttpRequest, queryset: QuerySet):
        context = {
            "vehicles": {
                q.name: request.build_absolute_uri(
                    reverse("vehicle_details", args=[q.pk])
                )
                for q in queryset
            }
        }
        return render(request, "admin/qr_codes.html", context)
