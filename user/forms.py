from django import forms
from django.contrib.auth.forms import UserChangeForm
from user.models import Profile
from django.contrib.auth.models import User


#profile updation form

class userUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)


class profileUpdateForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    profile_pic = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic',)


class MatricUpdateForm(forms.ModelForm):
    matric = forms.IntegerField(required=False, help_text='You wouldnt be able to change your matric number laterwhich can attract severe penalties. so enter your valid matric number')
    class Meta:
        model = Profile
        fields = ( 'matric',)

        
        