from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from search.util import keyword_search

def home(request):
	return render(request, 'search/index.html', {})

@csrf_exempt
def results(request):
	return render(request, 'search/results.html', keyword_search(request.POST['q']))
