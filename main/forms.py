from django import forms

from main.models import Defect, Trip


class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ["type", "comment", "reporter_name"]


class StartTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["starting_time", "starting_mileage", "driver_name", "purpose"]


class EndTripForm(forms.Form):
    starting_time = forms.DateTimeField(disabled=True, required=False)
    starting_mileage = forms.IntegerField(disabled=True, required=False)
    driver_name = forms.CharField(disabled=True, required=False)
    purpose = forms.CharField(disabled=True, required=False)
    ending_time = forms.DateTimeField()
    ending_mileage = forms.IntegerField()
