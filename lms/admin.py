from django.contrib import admin

from .models import Course, Module



class CourseAdmin(admin.ModelAdmin):
          prepopulated_fields = {"slug":("title",)}

class ModuleAdmin(admin.ModelAdmin):
          prepopulated_fields = {"slug":("title",)}

admin.site.register(Course,CourseAdmin)
admin.site.register(Module, ModuleAdmin)