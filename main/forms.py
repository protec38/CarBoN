from django import forms
from django.utils.translation import gettext as _
from django.utils import timezone

from main.models import Defect, Trip, FuelExpense


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"


class DateTimeLocalField(forms.DateTimeField):
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")


class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ["type", "comment", "reporter_name"]


class TripStartForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["starting_time", "starting_mileage", "driver_name", "purpose"]
        field_classes = {"starting_time": DateTimeLocalField}


class TripEndForm(forms.ModelForm):
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
