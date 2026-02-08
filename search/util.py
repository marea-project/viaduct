from api.models.arches import ArchesInstance, Concept
from django.core.cache import cache
import re, asyncio, hashlib

def strip_html_tags(text):
    return (re.sub(r'<.*?>', ' ', text)).strip()

def keyword_search(query_string):
    global results, ct, loop
    cache_key = hashlib.sha1(query_string.encode('utf8')).hexdigest()
    results = cache.get(cache_key)
    if not results is None:
        return results
    results = []
    ct = ArchesInstance.objects.count()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    def callback(fut):
        global results, ct, loop
        results = results + fut.result()
        ct = ct - 1
        if ct<= 0:
            loop.stop()
    futures = []
    for arches in ArchesInstance.objects.all():
        fut = asyncio.ensure_future(asyncio.to_thread(arches.search, query_string))
        fut.add_done_callback(callback)
        futures.append(fut)
    loop.run_forever()

    ret = []
    for x in sorted(results, key=lambda x: x['_score']):
        if not '_source' in x:
            continue
        if 'displaydescription' in x['_source']:
            x['_source']['displaydescription'] = strip_html_tags(x['_source']['displaydescription'])
        ret.append(x['_source'])
    cache.set(cache_key, ret, 300) # Cache the results for five minutes
    return ret

def concept_search(query_string):
    ret = []
    for concept in Concept.objects.filter(properties__value__icontains=query_string):
        ret.append({'pk': concept.pk, 'label': concept.label, 'uri': concept.uri, 'source': str(concept.thesaurus.instance)})
    return ret
