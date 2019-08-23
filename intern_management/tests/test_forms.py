from django.test import TestCase
from django.core import mail

from intern_management.forms import InternshipLogForm
from intern_management.models import InternshipLocationModel


class InternshipLogFormTests(TestCase):
    def setUp(self):
        InternshipLocationModel.objects.create(
            title="Test",
        )

    def test_form_mail(self):
        form = InternshipLogForm({
            'name': "Test",
            'hours': 10,
            'location': 1
        }, initial={
            'locations': InternshipLocationModel.objects.all().order_by(
                'title'
            ),
            'pk': InternshipLocationModel.objects.all().first().pk
        })
        self.assertTrue(form.is_valid())
        context = {
            'name': form.cleaned_data['name'],
            'location': form.cleaned_data['location'],
            'hours': form.cleaned_data['hours'],
            'domain': "test.com",
            'request_id': "fdsafa",
            'token': "test token",
        }
        form.send_mail(context, "testing@testing.com")

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(
            form.cleaned_data['name'] in mail.outbox[0].subject
            and form.cleaned_data['location'].title in mail.outbox[0].subject
        )
