from apartment.serializers import RatingSerializer
from rest_framework.views import APIView


class RatingView(APIView):
    def post(self, request):
        serialized = RatingSerializer(
            data=request.data, context={
                "request": "post"})
        if serialized.is_valid():
            serialized.save()
            response = {}
