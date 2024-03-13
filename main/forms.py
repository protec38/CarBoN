from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from main.models import Defect, Trip, FuelExpense


class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ["type", "comment", "reporter_name"]


class StartTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["starting_time", "starting_mileage", "driver_name", "purpose"]


class EndTripForm(forms.ModelForm):
    ending_time = forms.DateTimeField(required=True)
    ending_mileage = forms.IntegerField(required=True)
    update_initial = forms.BooleanField(initial=False)

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
