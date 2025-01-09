from django.urls import path

from main.views import (
    VehicleDetailView,
    VehicleListView,
    DefectCreateView,
    FuelExpenseCreateView,
    TripStartFormView,
    TripEndFormView,
    TripAbortFormView,
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
        "vehicles/<uuid:pk>/trip/start", TripStartFormView.as_view(), name="trip_start"
    ),
    path("vehicles/<uuid:pk>/trip/end", TripEndFormView.as_view(), name="trip_end"),
    path(
        "vehicles/<uuid:pk>/trip/abort", TripAbortFormView.as_view(), name="trip_abort"
    ),
]
