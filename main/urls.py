from django.urls import path

from main.views import VehicleDetailView

urlpatterns = [
    path(
        "vehicles/detail/<int:pk>/",
        view=VehicleDetailView.as_view(),
        name="vehicle_details",
    )
]
