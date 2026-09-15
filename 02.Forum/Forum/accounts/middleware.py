from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone


class CleanupExpiredRegistrationsMiddleware:
    """Deletes accounts that were never email-confirmed within the
    verification window (default 30 minutes).

    There's no background task runner (Celery, cron, etc.) set up for this
    project, so this sweeps expired, unconfirmed accounts lazily on every
    incoming request instead of on a fixed schedule. In practice this means
    an expired account disappears the next time *anyone* hits the site,
    which is close enough to real-time for a small app like this one.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._cleanup_expired()
        return self.get_response(request)

    def _cleanup_expired(self):
        User = get_user_model()
        timeout = timedelta(
            minutes=getattr(settings, "EMAIL_VERIFICATION_TIMEOUT_MINUTES", 30)
        )
        cutoff = timezone.now() - timeout
        User.objects.filter(
            is_active=False,
            email_verification__created_at__lt=cutoff,
        ).delete()
