from django.contrib import admin
from .models import *

# Register your models here.

class OasisInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'mrn', 'visit_date', 'cli_name_display', 'created_date', 'modified_date', 'completed')
    search_fields = ('name', 'mrn', 'cli_name')
    list_filter = ('cli_name', 'completed')
    ordering = ('-created_date',)
    list_per_page = 25

    def cli_name_display(self, obj):
        return obj.cli_name
    cli_name_display.short_description = 'Clinician Name'

admin.site.register(OasisInfo, OasisInfoAdmin)
admin.site.register(Image)

admin.site.site_header = "Pathwell OASIS Admin Panel"
admin.site.site_title = "Custom Admin Portal"
admin.site.index_title = "Welcome to the Pathwell OASIS Admin Portal"