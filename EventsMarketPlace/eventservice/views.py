import logging

from .models import Event
from django.core.cache import cache
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CreateEventSerializer
from .serializers import ListEventSerializer
from .serializers import QueryParamsSerializer

logger = logging.getLogger(__name__)


class EventListAPIView(APIView):

    def get_params(self):
        start_time = self.request.GET["starts_time"] if 'starts_time' in self.request.GET else None
        ends_time = self.request.GET["ends_time"] if 'ends_time' in self.request.GET else None
        
        if not all([start_time, ends_time]):
            logger.info("Missing 'start_time' or 'ends_time' fields")
        return start_time, ends_time

    @swagger_auto_schema(
        query_serializer=QueryParamsSerializer,
        responses={
            201: openapi.Response("Success response", ListEventSerializer),
            400: openapi.Response("Error response"),
        },
    )
    
    def get(self, request, *args, **kwargs):
        try:
            start_time, end_time = self.get_params()
            if start_time is not None and end_time is not None:
                events = Event.objects.in_datetime_range(start_time, end_time)
            else:
                events = Event.objects.all()
            serializered_events = ListEventSerializer(events, many=True)
            return Response({"data": {"events": serializered_events.data}})
        except Exception as ex:
            logger.error(f"Error processing request {ex}")
            raise APIException(code=400, detail=ex)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CreateEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def list_of_ids(request):
    last_data = cache.get("last_polled_ids")

    if last_data:
        logger.info("Returning data from cache")
        return JsonResponse(last_data, safe=False)
    logger.info("Updating data from DB")
    event_ids = Event.objects.values("base_event_id", "event_id")
    data = [
        f"{event.get('base_event_id')}:{event.get('event_id')}" for event in event_ids
    ]
    cache.set("last_polled_ids", data, timeout=600)
    return JsonResponse(data, safe=False)
