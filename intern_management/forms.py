from django import forms


class InternshipSignUpForm(forms.Form):
    location_name = forms.CharField(label="Location Name")
    location_address = forms.CharField(label="Address")
    location_email = forms.EmailField(label="Best Contact Email")
    location_website = forms.CharField(required=False, label="Location Wesite")


class InternshipLogForm(forms.Form):
    name = forms.CharField(label="Your Name")
    hours = forms.IntegerField(label="Hours to Log")
