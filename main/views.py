from __future__ import annotations

import datetime
import typing

import django.http
import django.shortcuts
import django.urls
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BooleanField, HiddenInput, ModelForm, BaseModelForm
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.db.models import Model

from . import forms, models


class VehicleListView(LoginRequiredMixin, ListView):
    model = models.Vehicle
    template_name = "main/vehicle_list.html"

    login_url = django.urls.reverse_lazy("admin:login")


class VehicleDetailView(DetailView):
    model = models.Vehicle
    context_object_name = "vehicle"
    template_name = "main/vehicle_detail.html"

    def get_context_data(self, **kwargs):
        self.object: models.Vehicle
        context = super().get_context_data(**kwargs)

        context["open_defects"] = context["vehicle"].open_defects.all()

        delegated_forms: dict[str, type[ModelForm]] = {
            "defect_form": forms.DefectForm,
            "fuel_expense_form": forms.FuelExpenseForm,
            "trip_start_form": forms.TripStartForm,
            "trip_end_form": forms.TripEndForm,
        }

        for variable_name, form in delegated_forms.items():
            if variable_name in self.request.session:
                context[variable_name] = form(
                    self.request.session[variable_name], vehicle=self.object
                )
                del self.request.session[variable_name]
            else:
                context[variable_name] = form(vehicle=self.object)

        try:
            current_trip = self.object.trip_set.get(finished=False)
            initial: dict[str, typing.Any] = {
                "starting_mileage": current_trip.starting_mileage,
                "starting_time": current_trip.starting_time,
                "driver_name": current_trip.driver_name,
                "purpose": current_trip.purpose,
                "ending_time": datetime.datetime.now(),
            }
            context["trip_end_form"].initial = initial
            context["trip_end_form"].instance.vehicle = self.object
            context["trip_started"] = True

        except models.Trip.DoesNotExist:
            # Pas de trajet en cours
            if context["trip_start_form"].is_bound:
                context["trip_start_form"].fields["force_validation"] = BooleanField(
                    initial=True, widget=HiddenInput()
                )

            context["trip_start_form"].instance.vehicle = self.object
            context["trip_started"] = False

        except models.Trip.MultipleObjectsReturned:
            raise models.Trip.MultipleObjectsReturned(
                _(
                    "Corruption de la base de données : plusieurs trajets sont en cours !"
                )
            )

        try:
            context["last_trip_distance"] = (
                self.object.trip_set.filter(finished=True)
                .latest("ending_time")
                .distance
            )
        except models.Trip.DoesNotExist:
            pass

        return context



GenericModel = typing.TypeVar("GenericModel", bound=Model)

class DelegationCreationView(CreateView, typing.Generic[GenericModel]):
    http_method_names = ["post"]
    success_message = ""
    variable_name = ""

    def get_success_url(self) -> str:
        return  django.urls.reverse_lazy(
            "vehicle_details", kwargs={"pk": self.kwargs.get("pk")}
        )

    def get_vehicle(self):
        return django.shortcuts.get_object_or_404(
            models.Vehicle, pk=self.kwargs.get("pk")
        )

    def post(self, request: django.http.HttpRequest, *args, **kwargs):
        form_class = typing.cast(type["BaseModelForm[GenericModel]"], self.form_class)
        
        form: BaseModelForm[GenericModel] = form_class(request.POST, vehicle=self.kwargs.get("pk"))
        form.instance.vehicle = self.get_vehicle()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form: BaseModelForm[GenericModel]):
        messages.info(self.request, self.success_message)

        return super().form_valid(form)

    def form_invalid(self, form):
        self.request.session[self.variable_name] = form.data
        return django.http.HttpResponseRedirect(
            self.get_success_url()
        )


class DefectCreateView(DelegationCreationView[models.Defect]):
    form_class = forms.DefectForm
    variable_name = "defect_form"
    success_message = _("L'anomalie a été signalée")


class FuelExpenseCreateView(DelegationCreationView[models.FuelExpense]):
    form_class = forms.FuelExpenseForm
    variable_name = "fuel_expense_form"
    success_message = _("Dépense de carburant sauvegardée")


class TripStartFormView(DelegationCreationView[models.Trip]):
    form_class = forms.TripStartForm
    variable_name = "trip_start_form"
    success_message = _("Début du trajet enregistré")

    def form_valid(self, form: "BaseModelForm[models.Trip]"):
        if models.Trip.objects.filter(finished=False, vehicle=self.kwargs.get("pk")).count() > 0:
            messages.error(
                self.request,
                _(f"Un trajet est déjà en cours !"),
            )
            return django.http.HttpResponseRedirect(
                django.urls.reverse_lazy(
                    "vehicle_details", kwargs={"pk": self.kwargs.get("pk")}
                )
            )

        else:
            return super().form_valid(form)


class TripEndFormView(UpdateView):
    http_method_names = ["post"]
    model = models.Trip
    form_class = forms.TripEndForm

    def get_success_url(self) -> str:
        return  django.urls.reverse_lazy(
            "vehicle_details", kwargs={"pk": self.kwargs.get("pk")}
        )

    def get_object(self, queryset=None):
        return models.Trip.objects.get(finished=False, vehicle=self.kwargs.get("pk"))

    def form_valid(self, form: "BaseModelForm[models.Trip]"):
        form.instance.finished = True
        form.save()
        distance = form.instance.ending_mileage - form.instance.starting_mileage

        messages.info(
            self.request,
            _(
                f'Le trajet suivant a été enregistré : {form.initial["purpose"].title()} - {distance} km'
            ),
        )

        return super().form_valid(form)
        

    def form_invalid(self, form: "BaseModelForm[models.Trip]"):
        self.request.session["trip_end_form"] = form.data
        return django.http.HttpResponseRedirect(self.get_success_url())


class TripAbortFormView(UpdateView):
    http_method_names = ["post"]
    model = models.Trip
    form_class = forms.TripEndForm

    def get_vehicle(self):
        return django.shortcuts.get_object_or_404(
            models.Vehicle, pk=self.kwargs.get("pk")
        )

    def post(self, request, *args, **kwargs):
        vehicle = self.get_vehicle()

        try:
            current_trip = vehicle.trip_set.get(finished=False)
            current_trip.finished = True
            current_trip.save()

            messages.info(self.request, _("Le trajet a été abandonné"))

            return django.http.HttpResponseRedirect(
                django.urls.reverse_lazy(
                    "vehicle_details", kwargs={"pk": self.kwargs.get("pk")}
                )
            )

        except models.Trip.DoesNotExist:
            ...
        except models.Trip.MultipleObjectsReturned:
            ...
