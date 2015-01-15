from django.shortcuts import render

def handler404(request):
	return render(request, '404.html')
