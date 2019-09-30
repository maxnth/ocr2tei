from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from users.models import CustomUser
from PIL import Image


class ProfilePictureUploader(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        image_file = request.data['file']

        try:
            img = Image.open(image_file)
            img.verify()
        except Exception as e:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        current_user = CustomUser.objects.get(id=request.user.id)
        current_user.profile_picture = image_file
        current_user.save()

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        current_user = CustomUser.objects.get(id=request.user.id)
        current_user.profile_picture = None
        current_user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
