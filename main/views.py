import datetime

import django.http
import django.urls
from django.views.generic import DetailView, ListView, CreateView
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext as _
import django.shortcuts

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

        if "defect_form" in self.request.session:
            context["defect_form"] = forms.DefectForm(self.request.session["defect_form"])
            del self.request.session["defect_form"]
        else:
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
                return django.http.HttpResponseServerError()

            context["trip_form"] = trip_form

        if "fuel_expense_form" not in context:
            context["fuel_expense_form"] = forms.FuelExpenseForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_data = dict()

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
                raise django.http.Http404(_(""))

            end_trip_form = forms.EndTripForm(request.POST, instance=current_trip)
            if end_trip_form.is_valid():
                if not end_trip_form.cleaned_data["update_initial"]:
                    end_trip_form.instance.starting_mileage = end_trip_form.initial[
                        "starting_mileage"
                    ]
                    end_trip_form.instance.starting_time = end_trip_form.initial[
                        "starting_time"
                    ]
                    end_trip_form.instance.purpose = end_trip_form.initial["purpose"]
                    end_trip_form.instance.driver_name = end_trip_form.initial[
                        "driver_name"
                    ]
                end_trip_form.instance.finished = True
                end_trip_form.save()

                end_trip_form.instance.vehicle.mileage = (
                    end_trip_form.instance.ending_mileage
                )
                end_trip_form.instance.vehicle.save()

                messages.info(self.request, _("Le trajet a été enregistré"))
            else:
                context_data["trip_form"] = end_trip_form
                context_data["trip_started"] = True

        if "abandon-trip-form" in self.request.POST:
            try:
                current_trip = self.object.trip_set.get(finished=False)
            except models.Trip.DoesNotExist:
                raise Http404(_(""))

            current_trip.finished = True
            current_trip.save()

            messages.info(self.request, _("Le trajet a été abandonné"))

        if "fuel-expense-form" in self.request.POST:
            fuel_expense_form = forms.FuelExpenseForm(request.POST)
            fuel_expense_form.instance.vehicle = self.object

            if fuel_expense_form.is_valid():
                fuel_expense_form.save()

                messages.info(self.request, _("Dépense de carburant sauvegardée"))
            else:
                context_data["fuel_expense_form"] = fuel_expense_form

        return self.render_to_response(self.get_context_data(**context_data))

class DefectCreateView(CreateView):
    http_method_names = ["post"]
    model = models.Defect
    form_class = forms.DefectForm

    def get_vehicle(self):
        return django.shortcuts.get_object_or_404(models.Vehicle, pk=self.kwargs.get("pk"))

    def form_valid(self, form):
        form.instance.vehicle = self.get_vehicle()
        form.save()
        messages.info(self.request, _("L'anomalie a été signalée"))
        return django.http.HttpResponseRedirect(django.urls.reverse_lazy("vehicle_details", kwargs={"pk": self.kwargs.get("pk")}))

    def form_invalid(self, form):
        self.request.session["defect_form"] = form.data
        return django.http.HttpResponseRedirect(django.urls.reverse_lazy("vehicle_details", kwargs={"pk": self.kwargs.get("pk")}))