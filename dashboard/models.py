from django.db import models
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.
class Dashboard(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    user = UserForeignKey(auto_user_add = True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)