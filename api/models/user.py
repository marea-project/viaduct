"""
User profile utilities and model extensions.

This module defines a UserProfile model (one-to-one with Django's built-in
User model) and a post-save signal handler that creates a profile for new users.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import datetime, os

def create_new_userprofile():
	"""
	Factory used as the default value for UserProfile.user_settings.

	:returns: an empty dictionary representing default settings
	:rtype: dict

	Example::

		>>> create_new_userprofile()
		{}
	"""
	ret = {}
	return ret

class UserProfile(models.Model):
	"""
	Per-user settings and profile extension.

	:param user: OneToOne relationship to Django's User model
	:type user: django.contrib.auth.models.User
	:param user_settings: JSON blob with user-specific preferences
	:type user_settings: dict

	The model exposes __getattr__ to look up values in user_settings or fall
	back to Django settings when appropriate.
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	user_settings = models.JSONField(default=create_new_userprofile, encoder=DjangoJSONEncoder)
	def __getattr__(self, name):
		"""
		Resolve unknown attributes by checking user_settings first, then
		project settings.

		:param name: attribute name to resolve
		:rtype: object or None
		"""
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
	"""
	Create or update a UserProfile when a User is saved.

	:param sender: the model class (User)
	:param instance: the instance being saved
	:param created: whether the instance was created
	"""
	if created:
		UserProfile.objects.create(user=instance)
	instance.profile.save()

