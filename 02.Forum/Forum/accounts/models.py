import random
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


def generate_code():
    """A random 6-digit confirmation code, e.g. '004821'."""
    return f"{random.randint(0, 999999):06d}"


class EmailVerification(models.Model):
    """Tracks the pending email confirmation for a newly registered
    (but not-yet-active) user. Deleted once the user confirms, or once the
    account itself is deleted by the cleanup middleware after it expires.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verification",
    )
    code = models.CharField(max_length=6, default=generate_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        timeout = timedelta(
            minutes=getattr(settings, "EMAIL_VERIFICATION_TIMEOUT_MINUTES", 30)
        )
        return timezone.now() > self.created_at + timeout

    def regenerate(self):
        self.code = generate_code()
        self.created_at = timezone.now()
        self.save(update_fields=["code", "created_at"])
