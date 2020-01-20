
from user.models import Profile

from django.views.generic import ListView






class HomeView(ListView):
	template_name = 'university/homepage.html'
	queryset = Profile.objects.all()
	context_object_name = 'profiles'



















