from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

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
    ending_time = forms.DateTimeField(label=_("Heure d'arrivée"))
    ending_mileage = forms.IntegerField(label=_("Kilométrage d'arrivée"))

    def clean(self):
        cleaned_data = super().clean()
        validation_errors = dict()

        if cleaned_data["ending_time"] <= cleaned_data["starting_time"]:
            validation_errors["ending_time"] = ValidationError(
                _("L'arrivée doit avoir lieu après le départ !")
            )

        if cleaned_data["ending_mileage"] < cleaned_data["starting_mileage"]:
            validation_errors["ending_mileage"] = ValidationError(
                _(
                    "Le kilométrage d'arrivée doit être supérieur ou égal au kilométrage de départ."
                )
            )

        raise ValidationError(validation_errors)
