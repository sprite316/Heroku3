from django.db import models


# Create your models here.
class MainList(models.Model):
    date = models.TextField(null=True)
    title = models.TextField(null=True)
    count = models.TextField(null=True)
    link = models.TextField(null=True)
    image = models.TextField(null=True)
    source = models.TextField(null=True)

    def __str__(self):
        return self.title
