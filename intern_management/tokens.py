import hashlib

from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.encoding import force_bytes


class UrlTokenGenerator:

    key_salt = "WGHS.IntershipManagement.App"
    secret = settings.SECRET_KEY

    def make_token(self, location, request):
        hash = salted_hmac(
            self.key_salt,
            self._make_hash_value(location, request),
            secret=self.secret,
        ).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.
        return hash

    def is_valid_token(self, location, request, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (token and location):
            print("Didn't give enough info")
            return False
        # validate token timestamp
        if not constant_time_compare(
            self.make_token(location, request),
            token
        ):
            print("Token failed to compare")
            return False
        return True

    def _make_hash_value(self, location, request):
        """
        Hash the user's primary key and some user state that's sure to change
        after a password reset to produce a token that invalidated when it's
        used:
        1. The password field will change upon a password reset (even if the
           same password is chosen, due to password salting).
        2. The last_login field will usually be updated very shortly after
           a password reset.
        Failing those things, settings.PASSWORD_RESET_TIMEOUT_DAYS eventually
        invalidates the token.

        Running this data through salted_hmac() prevents password cracking
        attempts using the reset token, provided the secret isn't compromised.
        """
        creation_timestamp = timezone.now().date() + timedelta(
            days=settings.URL_EXPIRE_DAYS
        )
        return (
               location.title
               + str(creation_timestamp)
               + request.id
               + str(request.is_valid)
        )


default_token_generator = UrlTokenGenerator()
