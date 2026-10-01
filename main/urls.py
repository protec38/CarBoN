from django.urls import path
from django.views.generic.base import RedirectView

from main.views import (
    DefectCreateView,
    FuelExpenseCreateView,
    TripStartFormView,
    TripUpdateView,
    VehicleDetailView,
    VehicleListView,
)

urlpatterns = [
    path(
        "vehicles/<uuid:pk>",
        view=VehicleDetailView.as_view(),
        name="vehicle_details",
    ),
    path("vehicles", VehicleListView.as_view(), name="vehicles_list"),
    path("vehicles/<uuid:pk>/defect", DefectCreateView.as_view(), name="defect"),
    path(
        "vehicles/<uuid:pk>/fuel-expense",
        FuelExpenseCreateView.as_view(),
        name="fuel_expense",
    ),
    path(
        "vehicles/<uuid:pk>/trip", TripStartFormView.as_view(), name="trip_start"
    ),
    path(
        "vehicles/<uuid:pk>/trip/<int:tpk>",
        TripUpdateView.as_view(),
        name="trip_update",
    ),
    path("", RedirectView.as_view(pattern_name="vehicles_list", permanent=True)),
]
