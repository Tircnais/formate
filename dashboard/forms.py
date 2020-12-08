#encoding:utf-8
from django import forms
# Para las cuenta de usuario (no administradores)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# se importan los modelos
from dashboard.models import *

class UsuarioForm(forms.ModelForm):
        class Meta:
                model = User
                fields = [
                        'first_name',
                        'last_name',
                        'email',
                        'username',
                        'password',
                        # 'password1',
                        # 'password2'
                ]
                labels = {
                        'first_name': 'Nombres',
                        'last_name': 'Apellidos',
                        'email': 'Correo electronico',
                        'username': 'Nombre de usuario',
                        # 'password': 'Ingrese su contraseña',
                        'password1': 'Ingrese su contraseña',
                        'password2': 'Confirme su contraseña'
                }
                widgets = {
                        'first_name': forms.TextInput(attrs={'class': 'form-control py-4', 'id':'inputFirstName', 'name':'first_name', 'required': 'True', 'placeholder': 'Ingrese su nombre'}),
                        'last_name': forms.TextInput(attrs={'class': 'form-control py-4', 'id':'inputLastName', 'name':'last_name', 'required': 'True', 'placeholder': 'Ingrese su apellido'}),
                        'email': forms.EmailInput(attrs={'class': 'form-control py-4', 'id':'inputEmailAddress', 'name':'email', 'required': 'True', 'placeholder': 'Ingrese su correo electronico'}),
                        'username': forms.TextInput(attrs={'class': 'form-control py-4', 'id':'inputuserName', 'name':'username', 'required': 'True', 'placeholder': 'Ingrese su nombre de usuario'}),
                        'password': forms.PasswordInput(attrs={'class': 'form-control py-4','id':'inputPassword', 'name':'password', 'required': 'True', 'placeholder': 'Ingrese su contraseña'}),
                        # 'password1': forms.PasswordInput(attrs={'class': 'form-control py-4','id':'inputPassword', 'name':'password1', 'required': 'True', 'placeholder': 'Ingrese su contraseña'}),
                        # 'password2': forms.PasswordInput(attrs={'class': 'form-control py-4','id':'inputConfirmPassword', 'name':'password2', 'required': 'True', 'placeholder': 'Confirme su contraseña'}),
                }
                help_texts = {
                        'email': 'Ingresa un correo valido para recuperar tu constraseña.',
                        # 'password2': 'Las constraseña deben coincidir.',
                }
                error_messages = {
                        # 'password2': {
                        #         'iguales': "Las constraseñas deben ser iguales.",
                        #         },
                }

        def save(self, commit=True):
                user = super().save(commit=False)
                user.set_password(self.cleaned_data['password'])
                if commit:
                        user.save()
                return user

class RegistroCompForm(forms.Form):
        class Meta:
                model = Competenciasusuario
                fields = [
                        'fkcompetence',
                        'tiene'
                ]
                labels = {
                        'fkcompetence':'Competencia digital',
                        'tiene': '¿Crees tener la competencia?'
                }
                help_texts = {
                        'fkcompetence': 'Seleccine la competencia deseada',
                        'tiene': 'Elije una opción o se guardara como <b>No</b>.',
                }
