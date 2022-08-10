from django.db import models

# Create your models here.


class Place(models.Model):
    name = models.TextField()


class Boundary(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    svg = models.TextField()


class Location(models.Model):
    name = models.TextField()
    category = models.TextField()
    svg = models.TextField()
    link = models.TextField(null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


