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
    starting_time = DateTimeLocalField(required=True, initial=timezone.now())

    class Meta:
        model = Trip
        fields = ["starting_time", "starting_mileage", "driver_name", "purpose"]


class TripEndForm(forms.ModelForm):
    starting_time = DateTimeLocalField(required=True)
    ending_time = DateTimeLocalField(required=True)
    ending_mileage = forms.IntegerField(required=True)
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


class FuelExpenseForm(forms.ModelForm):
    class Meta:
        model = FuelExpense
        fields = ("date", "mileage", "amount", "quantity")
