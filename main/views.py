from django.shortcuts import render
from django.views.generic import DetailView

from . import models


def details_view(request, id: int):
    pass


class VehicleDetailView(DetailView):
    model = models.Vehicle
    context_object_name = "vehicle"
