from django.conf import settings
from django.db import models


class Post(models.Model):
    """A forum post.

    'id' is Django's default auto-incrementing primary key: the first post
    created gets id=1, the second id=2, and so on -- this is the unique post
    number, no extra field needed for it.
    """

    name = models.CharField(max_length=64)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} {self.name}"


class Comment(models.Model):
    """A comment on a post. author is null for anonymous comments (shown
    as 'Anonymous' in templates) -- logged-out visitors are allowed to
    comment, they just aren't tied to an account."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        who = self.author.username if self.author else "Anonymous"
        return f"Comment by {who} on #{self.post_id}"
