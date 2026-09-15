from django.db import models


class Post(models.Model):
    #Forum posts model, including index, label (max 64 characters), contents and author
    index = models.IntegerField()
    label = models.CharField(max_length=64)
    contents = models.CharField()
    author = models.CharField()
    