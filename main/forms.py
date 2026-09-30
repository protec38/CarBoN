from django import forms
from django.utils.translation import gettext as _

from main.models import Defect, FuelExpense, Trip


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"


class DateTimeLocalField(forms.DateTimeField):
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")


class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ["comment", "reporter_name"]

    def __init__(self, *args, **kwargs):
        _ = kwargs.pop("vehicle", None)
        super().__init__(*args, **kwargs)


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["starting_mileage"]

    def __init__(self, *args, **kwargs):
        vehicle = kwargs.pop("vehicle", None)
        super().__init__(*args, **kwargs)
        if vehicle and not self.is_bound and not self.instance.pk:
            # Initialize starting_mileage with vehicle's current mileage
            self.fields["starting_mileage"].initial = vehicle.mileage


class TripStartForm(TripForm):
    class Meta(TripForm.Meta):
        model = Trip
        fields = ["starting_time", "starting_mileage", "driver_name", "purpose"]
        field_classes = {"starting_time": DateTimeLocalField}


class TripEndForm(TripForm):
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
        fields = ("date", "mileage", "amount", "quantity", "form_of_payment")

    def __init__(self, *args, **kwargs):
        vehicle = kwargs.pop("vehicle", None)
        super().__init__(*args, **kwargs)
        if vehicle and not self.is_bound and not self.instance.pk:
            self.fields["mileage"].initial = vehicle.mileage
