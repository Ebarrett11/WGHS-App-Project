from django.contrib import admin
from .models import InternshipLocationModel
# Register your models here.
admin.site.site_header = "WGHS Internship Management"


@admin.register(InternshipLocationModel)
class InternshipAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ('title', 'address', 'contact_email')
    search_fields = ['title', 'description']

    fieldsets = [
        (None, {
            'fields': ('title', 'address', 'manager')
        }),
        ('Description', {
            'classes': ['wide'],
            'fields': ('description',)
        }),
        ('Students', {
            'fields': ('students',)
        }),

    ]
