from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.contrib import messages

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'messages': messages.get_messages,
    })
    return env
