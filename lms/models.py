from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify


       

class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created', on_delete = models.CASCADE)
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=6)
    slug = models.SlugField()
    overview = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    student = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    course_image = models.FileField(blank=True, null=True)
    
    
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("lms:course_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save( *args, **kwargs)
    
    @property
    def mymodules(self):
        return self.modules.all()


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules',on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField()
    video_url = models.FileField(upload_to='videos', null=True)
    thumbnail = models.ImageField(blank=True, null=True)
    position = models.IntegerField()
    files = models.FileField(blank=True, null=True, default='default.jpg', upload_to = 'profile_pics')




    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("lms:module_detail", kwargs={"course_slug": self.course.slug,'module_slug':self.slug})

    # def get_update_url(self):
    #     return "/lms/edit/{}".format(self.id)
    # def get_delete_url(self):
    #     return "/lms/delete/{}".format(self.id)
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save( *args, **kwargs)






