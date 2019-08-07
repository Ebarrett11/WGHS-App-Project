from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
# Register your models here.
admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = "Profile"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
