from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Django's default help_text for "Password" is an HTML <ul> of
        # rules. A <p> can't legally contain a <ul>, so the browser
        # auto-closes the <p> (and the <span class="helptext"> inside it)
        # the moment it hits the <ul>, ejecting the whole list outside
        # .helptext -- it never picks up the chip styling used elsewhere.
        # Use the same rules as plain text instead, keeping the content
        # but rendering it as an ordinary single tip like every other
        # field.
        rules = password_validation.password_validators_help_texts()
        self.fields["password1"].help_text = " ".join(rules)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class LoginForm(AuthenticationForm):
    """Plain username + password login. Django's AuthenticationForm already
    does exactly this and authenticates against the hashed password."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # AuthenticationForm has no help text by default -- add tips under
        # both fields, matching the tip style used elsewhere (e.g. the
        # Username tip on the register page).
        self.fields["username"].help_text = (
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        )
        self.fields["password"].help_text = "Enter the password for your account."


class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        label="Confirmation code",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={"inputmode": "numeric", "autocomplete": "one-time-code"}
        ),
    )
