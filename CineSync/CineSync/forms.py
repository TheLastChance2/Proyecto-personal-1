from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core import validators
from django.contrib.auth.password_validation import CommonPasswordValidator, NumericPasswordValidator, validate_password



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu nombre de usuario'}),

    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'}),

        validators=[
            validators.MinLengthValidator(limit_value=8, message="La contraseña debe tener al menos 8 caracteres."),
            CommonPasswordValidator(),
            NumericPasswordValidator(),
            validators.ProhibitNullCharactersValidator(),
        ],
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirma tu contraseña'}),

        validators=[
            validate_password,
        ],
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']