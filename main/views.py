from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, CreateView
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.detail import SingleObjectMixin

from . import models
from . import forms


def details_view(request, id: int):
    pass


class VehicleDetailView(DetailView):
    model = models.Vehicle
    context_object_name = "vehicle"
    template_name = "main/vehicle_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["open_defects"] = context["vehicle"].defect_set.filter(
            status=models.Defect.DefectStatus.OPEN
        )

        if "defect_form" not in context:
            context["defect_form"] = forms.DefectForm()

        if "trip_form" not in context:
            try:
                current_trip = self.object.trip_set.get(finished=False)
                initial = {
                    "starting_mileage": current_trip.starting_mileage,
                    "starting_time": current_trip.starting_time,
                    "driver_name": current_trip.driver_name,
                    "purpose": current_trip.purpose,
                }
                trip_form = forms.EndTripForm(initial=initial)
                context["trip_started"] = True

            except models.Trip.DoesNotExist:
                # Pas de trajet en cours
                trip_form = forms.StartTripForm(
                    initial={"starting_mileage": self.object.mileage}
                )
                context["trip_started"] = False

            except models.Trip.MultipleObjectsReturned:
                return HttpResponseServerError()

            context["trip_form"] = trip_form

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "defect-form" in self.request.POST:
            defect_form = forms.DefectForm(request.POST)
            defect_form.instance.vehicle = self.object
            if defect_form.is_valid():
                defect_form.save()
                context_data = self.get_context_data(defect_created=True)
            else:
                context_data = self.get_context_data(defect_form=defect_form)

            return self.render_to_response(context_data)

        trip_form = None

        if "start-trip-form" in self.request.POST:
            start_trip_form = forms.StartTripForm(request.POST)
            start_trip_form.instance.vehicle = self.object
            if start_trip_form.is_valid():
                start_trip_form.save()
                context_data = self.get_context_data(trip_created=True)
            else:
                context_data = self.get_context_data(trip_form=start_trip_form)

        if "end-trip-form" in self.request.POST:
            try:
                current_trip = self.object.trip_set.get(finished=False)
            except models.Trip.DoesNotExist:
                ...

            end_trip_form = forms.EndTripForm(request.POST)
            if end_trip_form.is_valid():
                current_trip.ending_mileage = end_trip_form.cleaned_data[
                    "ending_mileage"
                ]
                current_trip.ending_time = end_trip_form.cleaned_data["ending_time"]
                current_trip.finished = True
                current_trip.save()

                current_trip.vehicle.mileage = current_trip.ending_mileage
                current_trip.vehicle.save()

                context_data = self.get_context_data(trip_edited=True)
            else:
                context_data = self.get_context_data(trip_form=trip_form)

        return self.render_to_response(context_data)
