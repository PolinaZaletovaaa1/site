
from django.db import models

from django.utils import timezone

import settings






class Article(models.Model):
    postdate = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(default='', null=True, max_length=50)
    description = models.TextField(default='', null=True)
    image = models.ImageField(upload_to='upload/')
    total_views = models.IntegerField(default =0 ,null=True)
