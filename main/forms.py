from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from main.models import Defect, Trip, FuelExpense


class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ["type", "comment", "reporter_name"]


class StartTripForm(forms.ModelForm):
    force_validate = forms.BooleanField(
        required=False, widget=forms.HiddenInput, initial=False
    )

    class Meta:
        model = Trip
        fields = [
            "starting_time",
            "starting_mileage",
            "driver_name",
            "purpose",
            "force_validate",
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("force_validate") is True:
            return

        validation_errors = dict()

        if cleaned_data["starting_mileage"] < self.instance.vehicle.mileage:
            validation_errors["starting_mileage"] = ValidationError(
                _(
                    "Le kilométrage de départ ne peut pas être inférieur au kilométrage du véhicule !"
                )
            )

        if (
            self.instance.ending_mileage
            and cleaned_data["starting_mileage"] > self.instance.ending_mileage
        ):
            validation_errors["ending_mileage"] = ValidationError(
                _(
                    "Le kilométrage de fin ne peut pas être inférieur au kilométrage de départ !"
                ),
                code="invalid",
            )

        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)


class EndTripForm(forms.ModelForm):
    starting_time = forms.DateTimeField(
        label=_("Heure de départ"), disabled=True, required=False
    )
    starting_mileage = forms.IntegerField(
        label=_("Kilométrage de départ"), disabled=True, required=False
    )
    driver_name = forms.CharField(
        label=_("Nom du conducteur"), disabled=True, required=False
    )
    purpose = forms.CharField(
        label=_("Motif du déplacement"), disabled=True, required=False
    )
    force_validate = forms.BooleanField(
        required=False, widget=forms.HiddenInput, initial=False
    )

    class Meta:
        model = Trip
        fields = [
            "starting_time",
            "starting_mileage",
            "driver_name",
            "purpose",
            "ending_time",
            "ending_mileage",
            "force_validate",
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("force_validate") is True:
            return
        validation_errors = dict()

        if (
            "ending_time" in cleaned_data
            and cleaned_data["ending_time"] <= cleaned_data["starting_time"]
        ):
            validation_errors["ending_time"] = ValidationError(
                _("L'arrivée doit avoir lieu après le départ !")
            )

        if (
            "ending_mileage" in cleaned_data
            and cleaned_data["ending_mileage"] < cleaned_data["starting_mileage"]
        ):
            validation_errors["ending_mileage"] = ValidationError(
                _(
                    "Le kilométrage d'arrivée doit être supérieur ou égal au kilométrage de départ."
                )
            )

        raise ValidationError(validation_errors)


class FuelExpenseForm(forms.ModelForm):
    class Meta:
        model = FuelExpense
        fields = ("date", "mileage", "amount", "quantity")
