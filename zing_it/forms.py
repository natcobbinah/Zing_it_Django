from django import forms
from .models import Song


class Signup(forms.Form):
    fullname = forms.CharField(required=True, max_length=255)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, required=True)


class Login(forms.Form):
    # email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, min_length=5)


class EditForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["track", "album", "artist", "length", "playlist"]
        exclude = []
