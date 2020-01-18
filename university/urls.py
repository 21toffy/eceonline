from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView
from lms.views import enroll, un_enroll
from django.conf.urls.static import static
from django.conf import settings



import lms.urls
import user.urls
import QA.urls


from . import views


urlpatterns = [

    path('QA/', include(QA.urls, namespace='questions')),

    path('', HomeView.as_view(), name='homepage'),

    path('admin/', admin.site.urls),

    path('lms/', include(lms.urls, namespace='lms')),

    path('profile/', include(user.urls, namespace='user')),


    path('accounts/', include('allauth.urls')),

    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('register/', views.signup, name='signup'),

    path('course/<slug:course_slug>/enroll', enroll, name='enroll_button'),
    path('course/<slug:course_slug>/unenroll', un_enroll, name='unenroll_button'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



