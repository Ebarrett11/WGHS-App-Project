from django import forms


class InternshipSignUpForm(forms.Form):
    location_name = forms.CharField(label="Location Name")
    location_address = forms.CharField(label="Address")
    location_email = forms.EmailField(label="Best Contact Email")
    location_website = forms.CharField(required=False, label="Location Wesite")


class InternshipLogForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=None,
        label="Location",
        empty_label="--Select Location--"
    )
    name = forms.CharField(label="Your Name")
    hours = forms.IntegerField(label="Hours to Log")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = kwargs['initial'].get('locations')

    def send_mail(self):
        pass
