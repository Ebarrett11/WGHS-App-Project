from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac


class UrlTokenGenerator:

    key_salt = "WGHS.IntershipManagement.App"
    secret = settings.SECRET_KEY

    def make_token(self, user, location):
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        hash = salted_hmac(
            self.key_salt,
            self._make_hash_value(user, location),
            secret=self.secret,
        ).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.
        return hash

    def check_token(self, user, location, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (user and token):
            return False
        # Parse the token

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, location), token):
            return False

        # Check the timestamp is within limit. Timestamps are rounded to
        # midnight (server time) providing a resolution of only 1 day. If a
        # link is generated 5 minutes before midnight and used 6 minutes later,
        # that counts as 1 day. Therefore, PASSWORD_RESET_TIMEOUT_DAYS = 1 means
        # "at least 1 day, could be up to 2."
        # if (self._num_days(self._today()) - ts) > settings.PASSWORD_RESET_TIMEOUT_DAYS:
        #     return False

        return True

    def _make_hash_value(self, user, location):
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
        # Truncate microseconds so that tokens are consistent even if the
        # database doesn't support microseconds.
        creation_timestamp = timezone.now().date() + timedelta(days=settings.URL_EXPIRE_DAYS)
        return str(user.pk) + str(user.username) + location.title + str(creation_timestamp)


default_token_generator = UrlTokenGenerator()
