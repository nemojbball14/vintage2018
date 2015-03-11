from django.views import generic
#for login required views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class HomeView(generic.TemplateView):
	"""Shows the timeline template."""
	template_name = 'timeline/home.html'

	#Remove after development finished
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(HomeView, self).dispatch(*args, **kwargs)