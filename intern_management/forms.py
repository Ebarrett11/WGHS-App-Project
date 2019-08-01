from django import forms
from django.core.mail import EmailMultiAlternatives
from django.template import loader


class InternshipSignUpForm(forms.Form):
    location_name = forms.CharField(label="Location Name")
    location_address = forms.CharField(label="Address")
    location_email = forms.EmailField(label="Best Contact Email")
    location_website = forms.CharField(required=False, label="Location Wesite")

    def send_mail(
            self, context, to_email,
            from_email=None,
            subject_template_name='emails/signup_email_subject.txt',
            email_template_name='emails/signup_email.html',
            html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()


class InternshipLogForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=None,
        label="Location",
        empty_label="--Select Location--",
    )
    name = forms.CharField(label="Your Name")
    hours = forms.IntegerField(label="Hours to Log")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        location_field = self.fields['location']
        location_field.queryset = kwargs['initial'].get('locations')
        location_field.initial = kwargs['initial'].get('pk')

    def send_mail(
            self, context, to_email,
            from_email=None,
            subject_template_name='emails/log_email_subject.txt',
            email_template_name='emails/log_email.html',
            html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
