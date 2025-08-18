from django import forms
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


from main.models import Defect, Trip, FuelExpense


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"


class DateTimeLocalField(forms.DateTimeField):
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")


class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ["type", "comment", "reporter_name"]


class BaseTripFrom:
    def clean(self):
        cleaned_data = super().clean()
        validation_errors = dict()
        if cleaned_data["starting_mileage"] < self.instance.vehicle.mileage:
            validation_errors["starting_mileage"] = ValidationError(
                _(
                    "Le kilométrage de départ ne peut pas être inférieur au kilométrage du véhicule !"
                ),
                code="invalid_mileage",
            )

        if (
            "ending_mileage" in cleaned_data
            and cleaned_data["starting_mileage"] > cleaned_data["ending_mileage"]
        ):
            validation_errors["ending_mileage"] = ValidationError(
                _(
                    "Le kilométrage de fin ne peut pas être inférieur au kilométrage de départ !"
                ),
                code="invalid_mileage",
            )

        if (
            "ending_time" in cleaned_data
            and cleaned_data["starting_time"] > cleaned_data["ending_time"]
        ):
            validation_errors["ending_time"] = ValidationError(
                _("L'arrivée doit avoir lieu après le départ !"), code="invalid_time"
            )

        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)

        return cleaned_data


class TripStartForm(BaseTripFrom, forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["starting_time", "starting_mileage", "driver_name", "purpose"]


class TripEndForm(BaseTripFrom, forms.ModelForm):
    update_initial = forms.BooleanField(
        initial=False, label="Modifier les infos de départ", required=False
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
        ]
        field_classes = {
            "starting_time": DateTimeLocalField,
            "ending_time": DateTimeLocalField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ending_time"].required = True
        self.fields["ending_mileage"].required = True


class FuelExpenseForm(forms.ModelForm):
    class Meta:
        model = FuelExpense
        widgets = {"date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}
        fields = ("date", "mileage", "amount", "quantity")
