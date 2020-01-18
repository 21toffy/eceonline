from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



LEVEL_CHOICE = (
('Year one','100'),
('Year two','200'),
('Year three','300'),
('Year four','400'),
('Year five','500'),
('POST GRADUATE','PGD'),
('Masters','MSc'),
)

   
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(choices=LEVEL_CHOICE, default='Year one', max_length=30)
    bio = models.CharField(max_length=200)
    profile_pic = models.ImageField(default='default.jpg', upload_to = 'profile_pics')
    matric = models.IntegerField(null=True,blank=True)
    is_teacher = models.BooleanField('teacher status', default=False)
    USERNAME_FIELD = 'matric'


    def __str__(self):
        return self.user.username

def post_save_profile(sender,instance,created,*args,**kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    profile,created = Profile.objects.get_or_create(user=instance)
post_save.connect(post_save_profile,User)

# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()