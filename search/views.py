from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def home(request):
	return render(request, 'search/index.html', {})

@csrf_exempt
def results(request):
	return render(request, 'search/results.html', request.POST)
