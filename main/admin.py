from __future__ import annotations

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from main.models import Defect, FuelExpense, Location, Setting, Trip, Vehicle


@admin.display(description=_("Nombre de véhicules"))
def vehicle_count(obj: Location):
    return obj.vehicle_set.count()


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", vehicle_count]


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = [
        "vehicle",
        "starting_time",
        "ending_time",
        "starting_mileage",
        "ending_mileage",
        "driver_name",
        "distance",
        "duration",
        "purpose",
        "finished",
    ]
    list_filter = ["vehicle", "starting_time"]


class DefectInline(admin.TabularInline):
    model = Defect
    extra = 0
    fields = (
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
        "parking_location",
        open_defect_count,
        "public_url",
        "mileage",
    ]
    inlines = [DefectInline]
    actions = ["get_qr_code"]
    list_editable = ["status", "parking_location"]

    @admin.action(description=_("Obtenir les QR codes"))
    def get_qr_code(self, request: HttpRequest, queryset: QuerySet["Vehicle"]):
        context = {
            "vehicles": [
                (
                    q.name,
                    q.registration_number,
                    request.build_absolute_uri(reverse("vehicle_details", args=[q.pk])),
                )
                for q in queryset
            ]
        }
        return render(request, "admin/qr_codes.html", context)


@admin.register(FuelExpense)
class FuelExpenseAdmin(admin.ModelAdmin):
    list_display = [
        "vehicle",
        "date",
        "mileage",
        "amount",
        "quantity",
        "form_of_payment",
    ]
    list_filter = ["vehicle", "date", "form_of_payment"]


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ["key", "value"]
    list_editable = ["value"]
    search_fields = ["key"]
    list_filter = ["key"]
