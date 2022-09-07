from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

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


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(TravelLocation, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    replies = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    comment_level = models.IntegerField(default=0)
    comment_group = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}: {self.user} -> {self.body[0:50]}"

    def reply_list(self):
        # TODO: We may need to order replies specially??
        print(Comment.objects.filter(Q(comment_level__gt=self.comment_level) & Q(comment_group=self.comment_group)))
        return Comment.objects.filter(Q(comment_level=self.comment_level + 1) & Q(comment_group=self.comment_group))

    def reply_indent(self):
        return self.comment_level * 20

    class Meta:
        ordering = ['-updated', '-created']


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(TravelLocation, on_delete=models.CASCADE)
