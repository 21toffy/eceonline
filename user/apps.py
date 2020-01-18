from django.apps import AppConfig
# from django.utils.translation import ugettext_lazy as _
# from django.db.models.signals import post_save
# from .signals import create_profile



class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        import user.signals

       

