from django import forms

class AutocompleteUserWidget(forms.TextInput):
    template_name = "main/widgets/autocomplete_user.html"

class AutocompletePurposeWidget(forms.TextInput):
    template_name = "main/widgets/autocomplete_purpose.html"