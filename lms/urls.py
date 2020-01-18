from .import views
from django.contrib import admin
from django.urls import path


from lms.views import CourseListView, CourseDetailView,ModuleDetailView, CourseModuleUpdateView, NewModuleView, NewModuleDeleteView, NewModuleUpdateView
from django.conf.urls import url
from . import views
    

app_name = 'lms'

urlpatterns = [
          path('', views.index, name='index'),
          path('course-list', views.CourseListView.as_view(), name  = 'course_list' ),
          path('course_detail/<slug>', views.CourseDetailView.as_view(), name  = 'course_detail' ),
          path('courses/<course_slug>/<module_slug>/', ModuleDetailView.as_view(), name='module_detail'),


          # path('module_detail/<slug:slug>', views.ModuleDetail.as_view(), name  = 'module_detail' ),



          path('create/',views.CourseCreateView.as_view(),name='course_create'),
          path('<pk>/edit/',views.CourseUpdateView.as_view(),name='course_edit'),
          path('<pk>/delete/',views.CourseDeleteView.as_view(),name='course_delete'),
          
          path('<pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),  
          path('module/<int:module_id>/', views.ModuleDetailView.as_view(), name='course_module'),

          # path('module_edit/',views.ModuleView,name='module_edit'),
          path('<id>/new_module/', NewModuleView, name='new_course_module'),


          path('delete/<int:id>/',NewModuleDeleteView ,name='module_to_delete'),
          path('edit/<int:id>/',NewModuleUpdateView,name='module_to_update'),




]