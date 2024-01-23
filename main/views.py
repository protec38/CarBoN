import datetime

from django.http import HttpResponseServerError, Http404
from django.views.generic import DetailView, ListView
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext as _

from . import models
from . import forms


class VehicleListView(ListView):
    model = models.Vehicle
    template_name = "main/vehicle_list.html"


class VehicleDetailView(DetailView):
    model = models.Vehicle
    context_object_name = "vehicle"
    template_name = "main/vehicle_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["open_defects"] = context["vehicle"].defect_set.filter(
            Q(status=models.Defect.DefectStatus.OPEN)
            | Q(status=models.Defect.DefectStatus.CONFIRMED)
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
                    "ending_time": datetime.datetime.now(),
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
        context_data = dict()

        if "defect-form" in self.request.POST:
            defect_form = forms.DefectForm(request.POST)
            defect_form.instance.vehicle = self.object
            if defect_form.is_valid():
                defect_form.save()
                messages.info(self.request, _("L'anomalie a été signalée"))
            else:
                context_data["defect_form"] = defect_form

        if "start-trip-form" in self.request.POST:
            start_trip_form = forms.StartTripForm(request.POST)
            start_trip_form.instance.vehicle = self.object
            if start_trip_form.is_valid():
                start_trip_form.save()

                messages.info(self.request, _("Début du trajet enregistré"))
            else:
                context_data["trip_form"] = start_trip_form

        if "end-trip-form" in self.request.POST:
            try:
                current_trip = self.object.trip_set.get(finished=False)
            except models.Trip.DoesNotExist:
                raise Http404(_(""))

            initial = {
                "starting_mileage": current_trip.starting_mileage,
                "starting_time": current_trip.starting_time,
                "driver_name": current_trip.driver_name,
                "purpose": current_trip.purpose,
            }
            end_trip_form = forms.EndTripForm(request.POST, initial=initial)
            if end_trip_form.is_valid():
                current_trip.ending_mileage = end_trip_form.cleaned_data[
                    "ending_mileage"
                ]
                current_trip.ending_time = end_trip_form.cleaned_data["ending_time"]
                current_trip.finished = True
                current_trip.save()

                current_trip.vehicle.mileage = current_trip.ending_mileage
                current_trip.vehicle.save()

                messages.info(self.request, _("Le trajet a été enregistré"))
            else:
                context_data["trip_form"] = end_trip_form
                context_data["trip_started"] = True

        if "fuel-expense-form" in self.request.POST:
            fuel_expense_form = forms.FuelExpenseForm(request.POST)
            fuel_expense_form.instance.vehicle = self.object

            if fuel_expense_form.is_valid():
                fuel_expense_form.save()

                messages.info(self.request, _("Dépense de carburant sauvegardée"))
            else:
                context_data["fuel_expense_form"] = fuel_expense_form

        return self.render_to_response(self.get_context_data(**context_data))
