from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'nome', 'email', 'bio', 'avatar']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'nome', 'email', 'bio', 'avatar']
