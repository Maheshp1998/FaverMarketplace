from uuid import uuid4

from common.models import TimeStampField
from django.core.cache import cache
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver


class EventQuerySet(models.QuerySet):
    def in_datetime_range(self, start_datetime, end_datetime):
        return self.filter(
            Q(start_date_time__gte=start_datetime) & Q(end_date_time__lte=end_datetime)
        )


class Event(TimeStampField):
    id = models.UUIDField(default=uuid4, primary_key=True)
    base_event_id = models.CharField(max_length=10)
    event_id = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    min_price = models.FloatField(default=0)
    max_price = models.FloatField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = [
            "created_at",
        ]

    def save(self, *args, **kwargs):
        if self.start_date_time:
            self.start_date = self.start_date_time.date()
            self.start_time = self.start_date_time.time()
        if self.end_date_time:
            self.end_date = self.end_date_time.date()
            self.end_time = self.end_date_time.time()
        # clears cache
        cache.delete("last_polled_ids")
        super(Event, self).save(*args, **kwargs)

    objects = EventQuerySet.as_manager()


@receiver(post_delete, sender=Event)
def clear_cache_on_delete(sender, instance, **kwargs):
    # clears cache
    cache.delete("last_polled_ids")


