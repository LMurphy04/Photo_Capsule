from django import forms
from django.contrib.auth.models import User
from photocapsule.models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profilePicture']

