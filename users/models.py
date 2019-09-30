from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    loaded_project = models.CharField(max_length=255, default=None, null=True)
    loaded_page = models.CharField(max_length=255, default=None, null=True)
    profile_picture = models.ImageField(upload_to="images/profile_pictures/",
                                        default="images/profile_pictures/default.png")

    editor_theme = models.CharField(max_length=255, default="monokai"
)
