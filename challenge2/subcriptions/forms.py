from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Usersignup(UserCreationForm):
    firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'firstname', 'id': 'name', 'name': 'firstname', 'type': 'text', 'class': 'input-field'}))
    lastname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last name', 'id': 'lastname', 'name': 'lastname', 'type': 'text', 'class': 'input-field'}))
    email = forms.CharField(widget=forms.TextInput(attrs={
                            'placeholder': 'Email', 'id': 'email1', 'name': 'email1', 'type': 'email', 'class': 'input-field'}))
    cardnumber = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'cardnumber', 'id': 'phnumber', 'name': 'cardnnumber', 'type': 'number', 'class': 'input-field'}))
    month = forms.CharField(widget=forms.TextInput(attrs={
                            'placeholder': 'month', 'id': 'month', 'type': 'number', 'name': 'month', 'class': 'input-fields'}))
    year = forms.CharField(widget=forms.TextInput(attrs={
                           'placeholder': 'year', 'id': 'year', 'type': 'number', 'name': 'year', 'class': 'input-fields'}))
    cvc = forms.CharField(widget=forms.TextInput(attrs={
                          'placeholder': 'cvc', 'id': 'cvc', 'type': 'number', 'name': 'cvc', 'class': 'input-fields'}))
