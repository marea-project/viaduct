from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from search.util import keyword_search, concept_search

def home(request):
	return render(request, 'search/index.html', {})

@csrf_exempt
def results(request):
	query = request.POST['q']
	mode = 'list'
	if 'category_map' in request.POST:
		mode = 'map'
	results = cache.get(query)
	if results is None:
		results = keyword_search(query)
		cache.set(query, results, 300) # Cache the results for five minutes
	concepts = concept_search(query)
	return render(request, 'search/results.html', {"query": query, "mode": mode, "results": results, "concepts": concepts})
