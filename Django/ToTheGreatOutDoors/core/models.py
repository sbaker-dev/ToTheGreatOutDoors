from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

import re

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
    map_x = models.FloatField()
    map_y = models.FloatField()

    def __str__(self):
        return self.name

    def short_name(self):
        """Allow for a shortened name for the account page"""
        if len(self.name) > 50:
            return self.name[0:50] + "..."
        return self.name

    def raw_name(self):
        return re.sub('[^A-Za-z0-9 ]+', '', self.name)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(TravelLocation, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    replies = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    comment_level = models.IntegerField(default=0)
    comment_group = models.IntegerField(default=0)
    parent = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.id}: {self.user} -> {self.body[0:50]}"

    def reply_list(self):
        return Comment.objects.filter(Q(comment_group=self.comment_group) &
                                      Q(location=self.location) &
                                      Q(comment_level=self.comment_level + 1) &
                                      Q(parent=self.id)
                                      )

    def reply_indent(self):
        return self.comment_level * 20

    class Meta:
        ordering = ['-updated', '-created', '-comment_group']


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(TravelLocation, on_delete=models.CASCADE)
