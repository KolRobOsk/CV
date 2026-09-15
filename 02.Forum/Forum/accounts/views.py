from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm, VerifyCodeForm

User = get_user_model()


def _verification_timeout_minutes():
    return getattr(settings, "EMAIL_VERIFICATION_TIMEOUT_MINUTES", 30)


def _send_verification_email(user, code):
    send_mail(
        subject="Confirm your Forum account",
        message=(
            f"Hi {user.username},\n\n"
            f"Your confirmation code is: {code}\n\n"
            f"Enter it on the verification page within "
            f"{_verification_timeout_minutes()} minutes, or your account "
            f"will be removed automatically and you'll need to register again."
        ),
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[user.email],
        fail_silently=False,
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            if getattr(settings, "EMAIL_VERIFICATION_ENABLED", True):
                # Inactive until the email code is confirmed; the cleanup
                # middleware removes the account if that never happens.
                user.is_active = False
                user.save()

                from .models import EmailVerification

                verification = EmailVerification.objects.create(user=user)
                _send_verification_email(user, verification.code)

                request.session["pending_user_id"] = user.pk
                return redirect("accounts:verify")

            # Email verification disabled: activate and log the user in
            # immediately. (See EMAIL_VERIFICATION_ENABLED in settings.py
            # to restore the confirmation-code flow above.)
            user.is_active = True
            user.save()
            auth_login(request, user)
            messages.success(request, "Welcome!")
            return redirect("homepage")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def verify_email(request):
    user_id = request.session.get("pending_user_id")
    user = User.objects.filter(pk=user_id, is_active=False).first() if user_id else None

    if not user or not hasattr(user, "email_verification"):
        messages.error(request, "Nothing to verify. Please register first.")
        return redirect("accounts:register")

    verification = user.email_verification

    if verification.is_expired():
        user.delete()
        request.session.pop("pending_user_id", None)
        messages.error(
            request,
            "Your confirmation code expired and the account was removed. "
            "Please register again.",
        )
        return redirect("accounts:register")

    if request.method == "POST":
        if "resend" in request.POST:
            verification.regenerate()
            _send_verification_email(user, verification.code)
            messages.success(request, "A new code has been sent to your email.")
            return redirect("accounts:verify")

        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["code"] == verification.code:
                user.is_active = True
                user.save(update_fields=["is_active"])
                verification.delete()
                request.session.pop("pending_user_id", None)
                auth_login(request, user)
                messages.success(request, "Email confirmed! Welcome.")
                return redirect("homepage")
            form.add_error("code", "Incorrect code.")
    else:
        form = VerifyCodeForm()

    return render(request, "accounts/verify.html", {"form": form, "email": user.email})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("homepage")

        # AuthenticationForm rejects inactive users without saying why.
        # Check separately so unconfirmed users get a useful message.
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        pending = User.objects.filter(username=username, is_active=False).first()
        if pending and pending.check_password(password):
            messages.error(request, "Please confirm your email before logging in.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    return redirect("homepage")


@login_required
def panel(request):
    return render(request, "accounts/panel.html")


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keeps the user logged in after their password (and therefore
            # session auth hash) changes.
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated.")
            return redirect("accounts:panel")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        auth_logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("homepage")

    return render(request, "accounts/delete_account.html")
