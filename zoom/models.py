from django.db import models

# Create your models here.

from django.db import models
from django_userforeignkey.models.fields import UserForeignKey


class Zoom(models.Model):
    idAccount = models.CharField(max_length=255, default=None)
    firstName = models.CharField(max_length=255, default=None)
    lastName = models.CharField(max_length=255, default=None)
    email = models.EmailField(
        max_length=254, unique=True, db_index=True, primary_key=True
    )
    meetingId = models.CharField(max_length=255, default=None)
    personalMeetingUrl = models.CharField(max_length=255, default=None)
    user = UserForeignKey(auto_user_add=True)

    class Meta:
        ordering = ("user",)

