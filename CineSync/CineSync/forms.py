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
        help_text=format_html(
        "<br>"
        "<ul>"
        "<li>Longitud máxima de 150 caracteres.</li>"
        "<li>Solo puede estar formado por letras, números y los caracteres @/./+/-/_.</li>"
        "</ul>"
    	)
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'}),
        help_text=(
            "<br>"
            "<ul>"
            "<li>La contraseña no puede ser similar a otros componentes de tu información personal.</li>"
            "<li>Debe contener al menos 8 caracteres.</li>"
            "<li>No puede ser una contraseña usada muy comúnmente.</li>"
            "<li>No puede estar formada exclusivamente por números.</li>"
            "</ul>"
        ),
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
        help_text=(
            "<ul>"
            "<li>Introduzca la misma contraseña nuevamente, para poder verificar la misma.</li>"
            "</ul>"
            ),
        validators=[
            validate_password,
        ],
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
