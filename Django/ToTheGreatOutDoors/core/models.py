from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class RasterMap(models.Model):
    place = models.TextField()
    x = models.FloatField()
    y = models.FloatField()
    size = models.FloatField()


class Boundary(models.Model):
    place = models.TextField()
    svg = models.TextField()


class TravelLocation(models.Model):
    name = models.TextField()
    category = models.TextField()
    svg = models.TextField()
    link = models.TextField(null=True)
    place = models.TextField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(TravelLocation, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-updated', '-created']