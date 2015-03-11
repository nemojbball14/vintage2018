from django.shortcuts import render

def handler404(request):
	"""Uses our custom '404.html' page."""
	return render(request, '404.html')
