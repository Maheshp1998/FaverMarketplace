from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "base_event_id",
        "event_id",
        "title",
        "start_date_time",
        "end_date_time",
    ]
