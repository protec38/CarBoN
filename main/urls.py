from django.urls import path

from main.views import VehicleDetailView, VehicleListView

urlpatterns = [
    path(
        "vehicles/detail/<int:pk>/",
        view=VehicleDetailView.as_view(),
        name="vehicle_details",
    ),
    path("vehicles/", VehicleListView.as_view(), name="vehicles_list"),
]
