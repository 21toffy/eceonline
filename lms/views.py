from django.views.generic import TemplateView,ListView,DetailView,View

from django.views.generic.edit import UpdateView, DeleteView, CreateView
from lms.models import Course, Module
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.forms.models import modelform_factory
from django.apps import apps
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.detail import DetailView


from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages

from .forms import ModuleFormSet
from django.forms.models import modelform_factory
from user.models import Profile

from .forms import ModuleForm
from django.views.generic.detail import DetailView
# from student.forms import CourseEnrollForm



def NewModuleView(request, id):
    course = get_object_or_404(Course,  id=id)
    form = ModuleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        new_module=form.save(commit=False)
        new_module.course=course
        new_module.save()
        return redirect('lms:course_list')
    return render(request, 'lms/new_module.html', context = {'form':form, 'course':course})

def NewModuleDeleteView(request, id):
    module_to_delete = get_object_or_404(Module,  id=id)
    # course_slug = module_to_delete.course.slug
    print(module_to_delete)
    module_to_delete.delete()
    return render(request,'university/homepage.html',{})


def NewModuleUpdateView(request, id):
    # course = get_object_or_404(Course,  id=id)
    module_to_update = get_object_or_404(Module,  id=id)
    form = ModuleForm(request.POST or None, request.FILES or None, instance = module_to_update)
    if form.is_valid():
        new_module=form.save(commit=False)
        # new_module.course=course
        new_module.save()
        return redirect('lms:course_list')
    return render(request, 'lms/new_module.html', context = {'form':form})



def enroll(request, course_slug):
    course = get_object_or_404 (Course, slug=course_slug)
    user = request.user
    course.student.add(user)
    print('you have been enrolled')
    return redirect('lms:course_detail',slug=course.slug)


def un_enroll(request, course_slug):
    course = get_object_or_404 (Course, slug=course_slug)
    user = request.user
    course.student.remove(user)
    print('you have been un-enrolled')
    return redirect('lms:course_detail',slug=course.slug)



def index(request):
    return redirect (request, 'university/homepage.html')




class CourseListView(ListView):
    model = Course
    template_name = 'lms/course_list.html' 
    paginate_by = 3
    qs = Course.objects.all()

  
    


class CourseDetailView(DetailView):
    template_name = 'lms/course_detail.html'
    model = Course





#################COURSE DETAILS####################

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(LoginRequiredMixin):
    model = Course

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)   


    
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['code', 'title', 'overview', 'course_image']
    success_url = reverse_lazy('lms:course_list')
    template_name = 'course/form.html'



class CourseCreateView(OwnerCourseEditMixin, CreateView):
    success_url = reverse_lazy('lms:course_list')
    permission_required = 'courses.add_course'


class CourseUpdateView( OwnerCourseEditMixin, UpdateView):
    success_url = reverse_lazy('lms:course_list')
    permission_required = 'courses.change_course'


class CourseDeleteView( OwnerCourseMixin, DeleteView):
    template_name = 'course/delete.html'
    success_url = reverse_lazy('lms:course_list')
    permission_required = 'courses.delete_course'



#####################################################
################## MUDULES ##########################
#####################################################





class OwnerModuleMixin(LoginRequiredMixin):
    model = Module


class OwnerModuleEditMixin(OwnerModuleMixin, OwnerEditMixin):
    fields=['title', 'description', 'video_url', 'files', 'title' ]
    success_url = reverse_lazy('lms:course_list')
    template_name = 'course/form.html'



class ManageModuleListView(OwnerModuleMixin, ListView):
    template_name = 'course/list.html'

class ModuleCreateView(PermissionRequiredMixin, OwnerModuleEditMixin, CreateView):
    success_url = reverse_lazy('lms:course_detail')
    permission_required = 'courses.add_course'


class ModuleUpdateView(OwnerModuleEditMixin, UpdateView):
    success_url = reverse_lazy('lms:course_detail')
    permission_required = 'courses.change_course'




class ModuleDeleteView(OwnerModuleMixin, DeleteView):
    template_name = 'course/delete.html'
    success_url = reverse_lazy('lms:course_detail')
    permission_required = 'courses.delete_course'



class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})



    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('lms:course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})




class ModuleDetailView(View,LoginRequiredMixin):
    def get(self, request, course_slug, module_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        module = get_object_or_404(Module, slug=module_slug)   
        context = {'module': module, 'course':course}
        return render(request, "lms/module_detail.html", context)





########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
######################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

########################################################################################################################
########################################################################################################################
########################################################################################################################

########################################################################################################################
########################################################################################################################
########################################################################################################################

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})



    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('lms:course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})





class CreateModuleView(LoginRequiredMixin, CreateView):
    form_class = ModuleForm
    template_name = 'university/module_edit.html'

    

    def get_initial(self):
        return {
            'course': self.get_course().id,
            # 'user': self.request.user.id,
        }

    def get_context_data(self, **kwargs):
        return super().get_context_data(course=self.get_course(), **kwargs)

    def get_success_url(self):
        return self.object.course.get_absolute_url()

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            # save and redirect as usual.
            return super().form_valid(form)
        

    def get_course(self):
        return Course.objects.get(pk=self.kwargs['pk'])