from django.forms import ModelForm, HiddenInput

from main.models import Defect


class DefectForm(ModelForm):
    class Meta:
        model = Defect
        fields = ["type", "comment", "reporter_name"]
