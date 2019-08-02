from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import StudentProfile
# Register your models here.
admin.site.unregister(User)


class StudentInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline,)
