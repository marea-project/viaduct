from ..models import GraphModel

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
