from django import forms
from django.forms import PasswordInput, TextInput, EmailInput, Textarea
from django.contrib.auth.forms import UserCreationForm
from .models import Messeges, User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Here'}))
    password1 = forms.CharField(required=True,label='Password', widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password Here'}))
    password2 = forms.CharField(required=True,label='Password Confirmation', widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password Again'}) )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter User Name Here'})
        }

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewMessegeform(forms.ModelForm):

    class Meta:
        model = Messeges
        fields = ['title', 'text']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Message Title Here'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Message Here','style': "resize:none"}),
        }


class verifyform(forms.ModelForm):

    class Meta:
        model = Messeges
        fields = ['title', 'text', 'C', 'S1', 'S2', 'S3', 'T1', 'T2', 'T3']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Message Title Here'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Message Here', 'rows':'5', 'style': "resize:none"}),
            'C': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter C'}),
            'S1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter S1'}),
            'S2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter S2'}),
            'S3': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter S3'}),
            'T1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter T1'}),
            'T2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter T2'}),
            'T3': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter T3'}),
        }


class loginform(forms.Form):
    username = forms.CharField(label='Username', max_length=1024, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter User Name Here'}), )
    password = forms.CharField(label='Password', max_length=1024, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password Here'}), )


class openform(forms.Form):
    T1 = forms.CharField(label='T1', max_length=1024, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter T1 Here'}), )
    T2 = forms.CharField(label='T2', max_length=1024, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter T2 Here'}), )