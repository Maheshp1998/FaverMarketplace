from rest_framework import serializers

from .models import Event


class ListEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class CreateEventSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = "__all__"


class QueryParamsSerializer(serializers.Serializer):
    starts_at = serializers.DateTimeField(required=False)
    ends_at = serializers.DateTimeField(required=False)
