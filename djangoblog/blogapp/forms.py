from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class createForm(forms.ModelForm):
    class Meta:
        model=article
        fields = [
            'title',
            'body',
            'image',
            'category'
        ]


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]


class GetAuthor(forms.ModelForm):
    class Meta:
        model=author
        fields = [
            'profile_picture',
            'details'
        ]


class GetComment(forms.ModelForm):
    class Meta:
        model=comment
        fields = [
            'email',
            'post_comment'
        ]


class UpdateAuthor(forms.ModelForm):
    class Meta:
        model=author
        fields = [
            'name',
            'profile_picture',
            'details'
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model=category
        fields = [
            'name'
        ]