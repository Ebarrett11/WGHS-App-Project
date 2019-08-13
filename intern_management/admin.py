from django.contrib import admin
from .models import InternshipLocationModel, LoggedHoursModel
# Register your models here.
admin.site.site_header = "WGHS Internship Management"


class LoggedHoursInline(admin.TabularInline):
    model = LoggedHoursModel
    fields = ('user', 'total_hours')
    readonly_fields = ("user",)
    extra = 0


@admin.register(InternshipLocationModel)
class InternshipAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ('title', 'address', 'contact_email')
    search_fields = ['title', 'description']
    inlines = [LoggedHoursInline]
    fieldsets = [
        (None, {
            'fields': ('title', 'address', 'managers', 'tags')
        }),
        ('Description', {
            'classes': ['wide'],
            'fields': ('description',)
        }),
        ('Students', {
            'fields': ('students',)
        }),

    ]
