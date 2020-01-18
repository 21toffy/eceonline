from django import forms
from django.contrib.auth.forms import UserChangeForm
from user.models import Profile
from django.contrib.auth.models import User

from user.models import Profile

from allauth.account.forms import SignupForm

from django import forms

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class userUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')


class profileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'level' )

      
      
class profileform(forms.ModelForm):
    matric = forms.IntegerField(help_text='You wouldnt be able to change your matric number laterwhich can attract severe penalties. so enter your valid matric number',required=False)
    class Meta:
        model =  Profile
        fields = ( 'matric', )


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='This information is Required.')
    password = forms.CharField(max_length=30,widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password' )