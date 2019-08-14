from django.contrib import admin
from .models import InternshipLocationModel, LoggedHoursModel
# Register your models here.
admin.site.site_header = "WGHS Internship Management"


class LoggedHoursInline(admin.TabularInline):
    model = LoggedHoursModel
    fields = ("id", "user", "total_hours", "is_valid")
    can_delete = True
    extra = 0


@admin.register(InternshipLocationModel)
class InternshipAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ('title', 'address', 'contact_email')
    search_fields = ['title', 'description']
    inlines = [LoggedHoursInline]
    fieldsets = [
        (None, {
            'fields': ('title', 'address', 'managers', 'tags', 'outstanding_tokens')
        }),
        ('Description', {
            'classes': ['wide'],
            'fields': ('description',)
        }),
        ('Students', {
            'fields': ('students',)
        }),

    ]
