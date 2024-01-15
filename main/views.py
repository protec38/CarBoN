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
                trip_form = forms.EndTripForm(instance=current_trip)
            except models.Trip.DoesNotExist:
                # Pas de trajet en cours
                trip_form = forms.StartTripForm(
                    initial={"starting_mileage": self.object.mileage}
                )
            except models.Trip.MultipleObjectsReturned:
                return HttpResponseServerError()

            context["trip_form"] = trip_form

            if isinstance(context["trip_form"], forms.StartTripForm):
                context["trip_started"] = False
            else:
                context["trip_started"] = True

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
            trip_form = forms.StartTripForm(request.POST)

        if "end-trip-form" in self.request.POST:
            try:
                current_trip = self.object.trip_set.get(finished=False)
            except models.Trip.DoesNotExist:
                ...

            trip_form = forms.EndTripForm(request.POST, instance=current_trip)
            trip_form.instance.finished = True

        if trip_form is not None:
            trip_form.instance.vehicle = self.object
            if trip_form.is_valid():
                trip_form.save()
                if trip_form.instance.finished:
                    self.object.mileage = trip_form.instance.ending_mileage
                    self.object.save()

                context_data = self.get_context_data(trip_edited=True)
            else:
                context_data = self.get_context_data(trip_form=trip_form)

            return self.render_to_response(context_data)
