import hashlib

from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.encoding import force_bytes


class UrlTokenGenerator:

    key_salt = "WGHS.IntershipManagement.App"
    secret = settings.SECRET_KEY

    def make_token(self, location, salt):
        hash = salted_hmac(
            self.key_salt,
            self._make_hash_value(location, salt),
            secret=self.secret,
        ).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.

        return hash

    def check_token(self, location, salt, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (token and location):
            return False
        # validate token timestamp
        if not constant_time_compare(
            self.make_token(location, salt),
            token
        ):
            return False

        # loop through locations valid tokens and compare them to given token
        location_tokens = location.outstanding_tokens
        tokens = location_tokens.split(':')
        token_hash = str(hashlib.sha256(force_bytes(token)).hexdigest())
        if token_hash in tokens:
            tokens.remove(token_hash)
            tokens_serialized = ":".join(tokens)
            location.outstanding_tokens = tokens_serialized
            location.save()
            return True

        return False

    def _make_hash_value(self, location, salt):
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
        creation_timestamp = timezone.now().date() + timedelta(days=settings.URL_EXPIRE_DAYS)
        return (
               location.title
               + str(creation_timestamp)
               + salt
        )


default_token_generator = UrlTokenGenerator()
