from django.urls import path

from main.views import VehicleDetailView, VehicleListView, DefectCreateView

urlpatterns = [
    path(
        "vehicles/<int:pk>",
        view=VehicleDetailView.as_view(),
        name="vehicle_details",
    ),
    path("vehicles", VehicleListView.as_view(), name="vehicles_list"),
    path("vehicles/<int:pk>/defect", DefectCreateView.as_view(), name="defect"),
]
