from django.forms import (
    ModelForm,
    DateTimeInput,
    NumberInput,
    TextInput,
)

from main.models import Defect, Trip


class DefectForm(ModelForm):
    class Meta:
        model = Defect
        fields = ["type", "comment", "reporter_name"]


class StartTripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ["starting_time", "starting_mileage", "driver_name", "purpose"]


class EndTripForm(ModelForm):
    class Meta:
        model = Trip
        fields = [
            "starting_time",
            "starting_mileage",
            "ending_time",
            "ending_mileage",
            "driver_name",
            "purpose",
        ]
        widgets = {
            "starting_time": DateTimeInput(attrs={"readonly": True}),
            "starting_mileage": NumberInput(attrs={"readonly": True}),
            "driver_name": TextInput(attrs={"readonly": True}),
            "purpose": TextInput(attrs={"readonly": True}),
            "ending_time": DateTimeInput(attrs={"required": True}),
            "ending_mileage": NumberInput(attrs={"required": True}),
        }
