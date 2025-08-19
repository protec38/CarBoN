from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

from main.models import Defect, FuelExpense, Trip


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"


class DateTimeLocalField(forms.DateTimeField):
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")


class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ["type", "comment", "reporter_name"]


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["starting_mileage"]

    def clean_starting_mileage(self):
        starting_mileage = self.cleaned_data["starting_mileage"]
        if starting_mileage < self.instance.vehicle.mileage:
            self.add_error(
                "starting_mileage",
                ValidationError(
                    _(
                        "Le kilométrage de départ ne peut pas être inférieur au kilométrage du véhicule !"
                    ),
                    code="invalid_mileage",
                ),
            )
        return starting_mileage


class TripStartForm(TripForm):
    class Meta(TripForm.Meta):
        model = Trip
        fields = ["starting_time", "starting_mileage", "driver_name", "purpose"]
        field_classes = {"starting_time": DateTimeLocalField}


class TripEndForm(TripForm):
    update_initial = forms.BooleanField(
        initial=False, label="Modifier les infos de départ", required=False
    )

    class Meta(TripForm.Meta):
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
