from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class InternshipLogForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=None,
        label="Location",
        empty_label="--Select Location--",
    )
    name = forms.CharField(label="Your Name")
    hours = forms.IntegerField(label="Hours to Log", validators=[
        MinValueValidator(1),
        MaxValueValidator(24)
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        location_field = self.fields['location']
        location_field.queryset = kwargs['initial'].get('locations')
        location_field.initial = kwargs['initial'].get('pk')
