from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from search.util import keyword_search, concept_search
import logging

logger = logging.getLogger(__name__)

def home(request):
	return render(request, 'search/index.html', {})

@csrf_exempt
def results(request):
	query = str(request.POST['q'])
	logger.info("Keyword search: " + query)
	mode = 'list'
	if 'category_map' in request.POST:
		mode = 'map'
	results = keyword_search(query)
	concepts = concept_search(query)
	return render(request, 'search/results.html', {"query": query, "mode": mode, "results": results, "concepts": concepts, "mapboxkey": settings.MAPBOX_KEY})
