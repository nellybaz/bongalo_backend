from rest_framework.views import APIView
from event.serializers import EventSerializer
from rest_framework.generics import ListAPIView
from event.models import Event
from rest_framework.response import Response
from rest_framework import status


class EventView(APIView):

    def get(self, request, *args, **kwargs):
        query = Event.objects.all()
        serializer = EventSerializer(query, many=True)
        return Response(status=status.HTTP_200_OK, data={
            "responseCode": 1,
            "data": serializer.data,
        })


class SingleEventView(APIView):

    def get(self, request, *args, **kwargs):
        event_id = self.request.query_params.get("event")
        if not Event.objects.filter(uuid=event_id).exists():
            return Response(status=status.HTTP_200_OK, data={
                "responseCode": 0,
                "message": "No event found"
            })

        query = Event.objects.get(uuid=event_id)
        serializer = EventSerializer(query)
        return Response(status=status.HTTP_200_OK, data={
            "responseCode": 1,
            "data": serializer.data,
        })

