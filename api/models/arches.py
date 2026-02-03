from django.db import models
from django.conf import settings
from django.core.validators import validate_slug
from django.contrib.auth.models import User
import uuid, requests

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

class ArchesLogin(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='arches_logins')
	instance = models.ForeignKey(ArchesInstance, on_delete=models.CASCADE, related_name='logins')
	username = models.CharField(max_length=128, null=False)
	password = models.CharField(max_length=128, null=False)
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

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
