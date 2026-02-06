from api.models.arches import ArchesInstance

def keyword_search(query_string):
    ret = {"results": [], "engines": []}
    for arches in ArchesInstance.objects.all():
        data = arches.search(query_string)
        if len(data) == 0:
            continue
        ret['results'] = ret['results'] + data
        ret['engines'].append(arches)
    ret['results'] = [x['_source'] for x in sorted(ret['results'], key=lambda x: x['_score'])]
    return ret
