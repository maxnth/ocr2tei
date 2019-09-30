from django.urls import path, include

from uploads import views

urlpatterns = [
    path('upload/profile_picture/<filename>', views.ProfilePictureUploader.as_view(), name='upload_profile_picture'),
]
