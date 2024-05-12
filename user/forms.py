from django import forms
from django.core.exceptions import ValidationError
from typing import Any

# from django.contrib.auth import authenticate

from user.models import Customer


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=255)

    class Meta:
        model = Customer
        fields: str = "__all__"

    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()
        password: str = cleaned_data.get("password", "")
        confirm_password: str = cleaned_data.get("confirm_password", "")

        if password != confirm_password:
            raise ValidationError("Passwords does not match")

        username: str = cleaned_data.get("username", "")
        if username.lower() in ["admin", "root"]:
            raise ValidationError("this username is not allowed")
        elif Customer.objects.filter(username=username).exists():
            raise ValidationError("username already exists")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=255)

    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()

        username: str = cleaned_data.get("username", "")
        password: str = cleaned_data.get("password", "")

        try:
            user: Customer = Customer.objects.get(username=username)

            if not user.check_password(password):
                raise ValidationError("username or password is incorrect")
            elif not user.is_active:
                raise ValidationError("This is user is inactive")
        except Customer.DoesNotExist:
            raise ValidationError("username or password is incorrect")

        cleaned_data["user"] = user
        return cleaned_data
