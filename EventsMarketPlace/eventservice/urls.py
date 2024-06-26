from django.urls import path

from .views import EventListAPIView, list_of_ids

app_name = "events"

urlpatterns = [
    path("", EventListAPIView.as_view(), name="list"),
    path("backend/ids", list_of_ids, name="id_list"),
]
