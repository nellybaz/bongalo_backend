from apartment.serializers import BookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BookingView(APIView):
    def post(self, request):
        serialized = BookingSerializer(
            data=request.data, context={
                "request": "post"})
        if serialized.is_valid():
            serialized.save()

            response_data = {"responseCode": 1, "data": serialized.data}
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = {"responseCode": 0, "data": serialized.errors}
        return Response(data=response_data, status=status.HTTP_200_OK)
