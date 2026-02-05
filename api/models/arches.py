from django.db import models
from django.conf import settings
from django.core.validators import validate_slug
from django.contrib.auth.models import User
from urllib.parse import urlencode
from rdflib import Graph
import uuid, requests, json

class ArchesInstance(models.Model):

	label = models.CharField(max_length=64, null=False)
	url = models.URLField(null=False)
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)
	def get_models(self):
		url = self.url.rstrip('/') + "/search_component_data/resource-type-filter"
		data = {}
		with requests.get(url, headers={'User-Agent': settings.USER_AGENT}) as r:
			data = r.json()
		if not 'resources' in data:
			return None
		return data['resources']
	def get_advanced_search_parameters(self):
		url = self.url.rstrip('/') + "/search_component_data/advanced-search"
		with requests.get(url, headers={'User-Agent': settings.USER_AGENT}) as r:
			return r.json()
	def get_collections(self):
		url = self.url.rstrip('/') + "/concepts/tree/collections"
		with requests.get(url, headers={'User-Agent': settings.USER_AGENT}) as r:
			return r.json()
	def get_thesauri(self):
		url = self.url.rstrip('/') + "/concepts/tree/semantic"
		with requests.get(url, headers={'User-Agent': settings.USER_AGENT}) as r:
			return r.json()
	def search(self, query_string):
		filter = [{'inverted': False, 'type': 'string', 'context': '', 'context_label': '', 'id': query_string, 'text': 'Contains Term: ' + query_string, 'value': query_string, 'selected': True}]
		query = {'paging-filter': '1', 'tiles': 'true', 'format': 'tilecsv', 'reportlink': 'true', 'language': '*', 'term-filter': json.dumps(filter)}
		url = self.url.rstrip('/') + "/search/resources?" + urlencode(query)
		data = {}
		with requests.get(url, headers={'User-Agent': settings.USER_AGENT}) as r:
			data = r.json()
		if not 'results' in data:
			return []
		if not 'hits' in data['results']:
			return []
		if not 'hits' in data['results']['hits']:
			return []
		return data['results']['hits']['hits']
	
	def __str__(self):
		return self.label

class ArchesLogin(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='arches_logins')
	instance = models.ForeignKey(ArchesInstance, on_delete=models.CASCADE, related_name='logins')
	username = models.CharField(max_length=128, null=False)
	password = models.CharField(max_length=128, null=False)
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user + ' / ' + str(self.instance)

	class Meta:
		unique_together = ('user', 'instance',)

class GraphModel(models.Model):

	instance = models.ForeignKey(ArchesInstance, on_delete=models.CASCADE, related_name='models')
	graphid = models.UUIDField(default=uuid.uuid4)
	name = models.CharField(max_length=128, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	version = models.TextField(blank=True, null=True)
	iconclass = models.TextField(blank=True, null=True)
	color = models.TextField(blank=True, null=True)
	subtitle = models.TextField(blank=True, null=True)
	slug = models.TextField(validators=[validate_slug])
	config = models.JSONField(db_column="config", default=dict)
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('instance', 'graphid',)

	def __str__(self):
		return str(self.instance) + ' / ' + self.name

class Thesaurus(models.Model):

	instance = models.ForeignKey(ArchesInstance, on_delete=models.CASCADE, related_name='thesauri')
	thesaurusid = models.UUIDField(default=uuid.uuid4)
	label = models.CharField(max_length=128, default='')
	labelid = models.UUIDField(null=True, blank=True)
	load_on_demand = models.BooleanField(default=False)

	class Meta:
		unique_together = ('instance', 'thesaurusid',)

	def __str__(self):
		return str(self.instance) + ' / ' + self.label
	
	@property
	def skos_url(self):
		return self.instance.url + 'concepts/export/' + str(self.thesaurusid)
	
	def load_skos(self):
		g = Graph()
		g.parse(self.skos_url, format='xml')
		return g

class Concept(models.Model):

	thesaurus = models.ForeignKey(Thesaurus, on_delete=models.CASCADE, related_name='concepts')
	conceptid = models.UUIDField(default=uuid.uuid4)

	@property
	def label(self):
		label = self.properties.filter(property='prefLabel', lang__startswith='en').first()
		if label:
			return str(label.value)
		return self.conceptid

	class Meta:
		unique_together = ('thesaurus', 'conceptid',)

	def __str__(self):
		return str(self.thesaurus) + ' / ' + str(self.label)

class ConceptProperty(models.Model):

	subject = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='properties')
	property = models.SlugField(max_length=128)
	value = models.TextField(default='')
	type = models.SlugField(max_length=64, default='literal')
	lang = models.SlugField(max_length=64, default='en')

class ConceptPredicate(models.Model):

	subject = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='predicates')
	property = models.SlugField(max_length=128)
	object = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='predicates_rev')
