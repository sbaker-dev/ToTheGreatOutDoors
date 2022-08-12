from django.db import models

# Create your models here.


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


