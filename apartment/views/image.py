from apartment.serializers import ImageSerializer
from rest_framework.views import APIView
from apartment.models import Apartment, Images
from rest_framework.response import Response
from rest_framework import status


class ImageView(APIView):
    def post(self, request):
        serialized = ImageSerializer(
            data=request.data, context={
                "request": "post"})

        if serialized.is_valid():
            serialized.save()
            response_data = {"responseCode": 1, "data": serialized.data}

            return Response(data=response_data, status=status.HTTP_201_CREATED)

        response_data = {"responseCode": 0, "data": serialized.errors}

        return Response(data=response_data, status=status.HTTP_200_OK)

    def get(self, request):
        apartment = self.request.query_params.get("apartment")

        if not Apartment.objects.filter(uuid=apartment).exists():
            response_data = {
                "responseCode": 0,
                "data": "apartment does not exist"}

            return Response(data=response_data, status=status.HTTP_200_OK)

        apartment_obj = Images.objects.filter(apartment=apartment)
        serialized = ImageSerializer(
            apartment_obj, context={
                "request": "post"}, many=True)

        if serialized:
            response_data = {"responseCode": 1, "data": serialized.data}

            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data = {"responseCode": 0,
                         "data": serialized.errors,
                         'message': 'Error occurred'}

        return Response(data=response_data,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        image = self.request.data.get("image")
        apartment = self.request.data.get("apartment")

        if image is None or apartment is None:
            response_data = {
                    "responseCode": 0,
                    "message": "Apartment UUID and Image URL are both required"
                    }

            return Response(data=response_data,
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            image_obj = Images.objects.filter(image=image, apartment=apartment)

            if image_obj.exists():
                result = image_obj.delete()

                if result:
                    response_data = {
                        "responseCode": 1,
                        "message": "Image has been deleted"}

                    return Response(data=response_data,
                                    status=status.HTTP_200_OK)
            else:
                response_data = {
                    "responseCode": 0,
                    "message": "Image does not exist"}

                return Response(data=response_data,
                                status=status.HTTP_404_NOT_FOUND)
