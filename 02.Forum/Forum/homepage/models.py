from django.db import models


class Post(models.Model):
    """A forum post.

    'id' is Django's default auto-incrementing primary key: the first post
    created gets id=1, the second id=2, and so on -- this is the unique post
    number, no extra field needed for it.
    """

    name = models.CharField(max_length=64)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} {self.name}"
