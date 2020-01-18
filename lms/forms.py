from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module



class ModuleForm(forms.ModelForm):
    Course = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Course.objects.all(),
        disabled=True,
    )

    class Meta:
        model = Module
        fields = ['title', 'description','position','video_url','files','course',]
    

    class Meta:
        model = Module
        exclude = ()

ModuleFormSet = inlineformset_factory(Course, Module, form=ModuleForm, fields=['title', 'description','position','video_url','files',], extra=2, can_delete=True)




class ModuleForm(forms.ModelForm):
        course = forms.ModelChoiceField(
                widget=forms.HiddenInput,
                queryset=Course.objects.all(),
                disabled=True,
                required=False,
    )
        class Meta:
                model = Module
                fields=['title', 'description', 'video_url', 'files', 'position','course' ]







