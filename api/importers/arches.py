from rdflib.namespace import RDF, SKOS
from ..models import GraphModel, Thesaurus, Concept, ConceptPredicate, ConceptProperty
import json

def load_instance_models(arches):

	for item in arches.get_models():
		try:
			model = GraphModel.objects.get(instance=arches, graphid=item['graphid'])
		except:
			model = GraphModel(instance=arches, graphid=item['graphid'])
		model.name = item['name']
		model.description = item['description']
		model.version = item['version']
		model.iconclass = item['iconclass']
		model.color = item['color']
		model.subtitle = item['subtitle']
		model.slug = item['slug']
		model.config = item['config']
		if model.slug is None:
			model.slug = ''
		model.save()


# dict_keys(['author', 'color', 'config', 'deploymentdate', 'deploymentfile',
# 'description', 'disable_instance_creation', 'functions', 'graphid', 'iconclass',
# 'isresource', 'jsonldcontext', 'name', 'ontology_id', 'publication_id', 'slug',
# 'subtitle', 'template_id', 'version'])

#        instance = models.ForeignKey(ArchesInstance, on_delete=models.CASCADE, related_name='models')
#        graphid = models.UUIDField(default=uuid.uuid4)
#        name = models.CharField(max_length=128, blank=True, null=True)
#        description = models.TextField(blank=True, null=True)
#        version = models.TextField(blank=True, null=True)
#        iconclass = models.TextField(blank=True, null=True)
#        color = models.TextField(blank=True, null=True)
#        subtitle = models.TextField(blank=True, null=True)
#        slug = models.TextField(validators=[validate_slug])
#        config = models.JSONField(db_column="config", default=dict)
#        created_time = models.DateTimeField(auto_now_add=True)
#        updated_time = models.DateTimeField(auto_now=True)

def load_instance_thesauri(arches):

	for item in arches.get_thesauri():
		try:
			thesaurus = Thesaurus.objects.get(instance=arches, thesaurusid=item['id'])
		except:
			thesaurus = Thesaurus(instance=arches, thesaurusid=item['id'])
		thesaurus.label = item['label']
		thesaurus.labelid = item['labelid']
		thesaurus.load_on_demand = item['load_on_demand']
		thesaurus.save()

def __convert_arches_skos_to_string(value):

	try:
		lang = value.language
	except:
		lang = 'en'
	try:
		parsed_value = json.loads(str(value))
	except json.decoder.JSONDecodeError:
		parsed_value = value
	if isinstance(parsed_value, str):
		return (parsed_value, lang)
	if isinstance(parsed_value, dict):
		if 'value' in parsed_value:
			return (parsed_value['value'], lang)
	return (str(value), lang)

def import_thesaurus(thesaurus):

	g = thesaurus.load_skos()
	concepts = []
	for concept, p, o in g.triples((None, RDF.type, SKOS.Concept)):
		concepts.append(concept)
	for concept in concepts:
		print(concept)
		print('  Properties')
		for s, p, o in g.triples((concept, None, None)):
			if o.__class__.__name__ == 'URIRef':
				continue
			value, lang = __convert_arches_skos_to_string(o)
			print('    ' + str(p) + ': ' + value + ' @ ' + lang)
		print('  Predicates')
		for s, p, o in g.triples((concept, None, None)):
			if not o.__class__.__name__ == 'URIRef':
				continue
			print('    ' + str(p) + ': ' + str(o))
