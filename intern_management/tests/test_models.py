from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from intern_management.models import (
    InternshipLocationModel,
    LoggedHoursModel
)


class InternshipLocationModeTests(TestCase):
    def setUp(self):
        InternshipLocationModel.objects.create(
            title="Title",
            address="Dummy",
            description="Dummy Data",
            contact_email="test@test.com",
        )

    def test_title(self):
        x = InternshipLocationModel.objects.get(pk=1)
        self.assertEqual(str(x), x.title)

    def test_absolute_url(self):
        x = InternshipLocationModel.objects.get(pk=1)
        self.assertEqual(
            x.get_absolute_url(), reverse(
                "intern_management:location_details",
                kwargs={
                    "pk": x.pk
                }
            )
        )


class LoggedHoursModelTests(TestCase):
    def setUp(self):
        User.objects.create(
            username="Luke"
        )
        InternshipLocationModel.objects.create(
            title="Title",
            address="Dummy",
            description="Dummy Data",
            contact_email="test@test.com",
        )
        LoggedHoursModel.objects.create(
            user=User.objects.get(pk=1),
            total_hours=10,
            location=InternshipLocationModel.objects.first(),
            id="Max2013"
        )

    def test_title(self):
        x = LoggedHoursModel.objects.get(id="Max2013")
        self.assertEqual(str(x), "Logged Hours for " + x.user.username)
