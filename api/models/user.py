from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import datetime, os

def create_new_userprofile():
	ret = {}
	return ret

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	user_settings = models.JSONField(default=create_new_userprofile, encoder=DjangoJSONEncoder)
	def __getattr__(self, name):
		if name in self.user_settings:
			return self.user_settings['name']
		try:
			return getattr(settings, name)
		except:
			return None
	def __str__(self):
		return str(self.user)

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
	instance.profile.save()

