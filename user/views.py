from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from user.models import Profile
from django.contrib.auth.models import User

from django.contrib import messages
from django.views.generic import TemplateView,ListView,DetailView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import userUpdateForm, profileUpdateForm, MatricUpdateForm
from lms.models import Course, Module
























@login_required
def Profile_Page(request):
    print(request.user.id)
    profile = get_object_or_404(Profile, id=request.user.id)
    context={'profile':profile, 'my_courses':my_courses, 'user':user}
    return render(request,'university/profile_page.html',context)



def get_user_profile(request):
    user_profile_qs = Profile.objects.filter(user=request.user)
    return user_profile_qs.first()

def get_user_courses(request):
    user_courses_qs = request.user.courses_joined.values()
    return user_courses_qs



def get_teachers_courses(request):
    teachers_courses_qs = request.user.courses_created.all()
    return teachers_courses_qs



@login_required
def myprofile(request):
    user_profile = get_user_profile(request)
    user_courses = get_user_courses(request)
    # teachers_courses = get_teachers_courses(request)
    teachers_courses= Course.objects.filter(owner=request.user)
    if request.method== 'POST':
        u_form = userUpdateForm(request.POST,instance=request.user)
        p_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        # profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully',
            extra_tags='alert alert-success  alert-dismissible fade show')
            return redirect('user:profile')
        else:
            messages.error(request, 'Error updating your profile', extra_tags='alert alert-error  alert-dismissible fade show')
            return redirect('user:profile')
    else:
        u_form = userUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user) 

    context= {
        
        'user_profile':user_profile,
        'user_courses':user_courses,
        'teachers_courses':teachers_courses,
        'u_form':u_form,
        'p_form':p_form,
    }
    return render(request,'profile/profile.html',context)




def matric_edit_view(request, id):
    user = get_object_or_404(Profile, id=id)
    if request.user !=Profile.user:
        return redirect('/')
        
    if request.method=='POST':
        m_form = MatricUpdateForm(request.POST, instance=request.user)
        if m_form.is_valid():
            form = m_form.save(commit=False)
            form.user = user
            form.save()
            messages.success(request, 'matric number updated successfully ',
            extra_tags='alert alert-success  alert-dismissible fade show')
        else:
            messages.error(request, 'Error your matric number has to ba in the form 140211***')
        return redirect('account_login')
    else:
        m_form = MatricUpdateForm(instance=request.user)
    context= {'m_form':m_form,}
    return render(request,'university/edit_matric.html',context)

    


###this is for a custom userform so that a blank profie can be created in other to avoid empty querying when checking a profile
# Profile.objects.create(user=new_user)
    