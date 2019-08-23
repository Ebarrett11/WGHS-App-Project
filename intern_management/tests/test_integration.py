from django.test import TestCase
from django.contrib.auth.models import User

from ..models import InternshipLocationModel
from ..tokens import default_token_generator


class TestTokenValidation(TestCase):
    """
        Description:
            Tests for token validation
    """

    def setUp(self):
        location = InternshipLocationModel.objects.create(
            title="Testing Location",
            outstanding_tokens=''
        )
        location.loggedhoursmodel_set.create(
            total_hours=5,
            user=User.objects.create(
                username="test"
            ),
            id="1"
        )
        location.loggedhoursmodel_set.create(
            total_hours=2,
            user=User.objects.create(
                username="test2"
            ),
            id="2"
        )

    def test_token_match(self):
        """
            Description:
                Tokens should be valid if matched with the right request within the standard time allowed
        """
        location = InternshipLocationModel.objects.get(pk=1)
        request = location.loggedhoursmodel_set.get(id=1)

        token = default_token_generator.make_token(location, request)
        default_token_generator.assign_token(token, location)

        self.assertTrue(
            default_token_generator.is_valid_token(
                location, request, token
            )
        )

    def test_token_reject(self):
        """
            Description:
                Tokens should not be valid for another request than the one it
                was made for
        """
        location = InternshipLocationModel.objects.get(pk=1)
        request1 = location.loggedhoursmodel_set.get(id=2)
        request2 = location.loggedhoursmodel_set.get(id=1)

        token = default_token_generator.make_token(location, request1)
        default_token_generator.assign_token(token, location)
        self.assertFalse(
            default_token_generator.is_valid_token(
                location, request2, token
            )
        )

    def test_token_with_too_little_info(self):
        """
            Description:
                Token must have enough info to compare
        """
        self.assertFalse(
            default_token_generator.is_valid_token(None, None, None)
        )

    def test_token_location_mismatch(self):
        """
            Description:
                Token must have been assigned to accessed Location
        """
        location = InternshipLocationModel.objects.get(pk=1)
        request = location.loggedhoursmodel_set.get(id=1)
        token = default_token_generator.make_token(location, request)
        self.assertFalse(
            default_token_generator.is_valid_token(
                location, request, token
            )
        )
