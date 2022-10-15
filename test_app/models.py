from django.conf import settings
from django.db import models


class Url(models.Model):
    default_url = models.URLField(max_length=2555)
    short_url = models.URLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
