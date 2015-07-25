from django.db import models
from django.contrib.auth.models import User
from positions.models import Position, Organisation
from offers.models import Offer

ENTITIES = [
	(1, User),
	(2, Position),
	(3, Organisation),
	(4, Offer)
]

# Create your models here.
class Note(models.Model):
	author = models.ForeignKey(User)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	date_deleted = models.DateTimeField(null=True, blank=True)
	deleter = models.ForeignKey(User, null=True, blank=True, related_name="deleted_notes")
	message = models.TextField()
	entity_type = models.IntegerField()
	entity_id = models.PositiveIntegerField()

	class Meta:
		ordering = ('date_created',)

	def get_author_name(self):
		"""Get the full name of the author, or if they don't have one, just return the author object itself (which will render as the author's username)"""
		name = self.author.get_full_name()

		if name:
			return name
		else:
			return self.author

	def get_deleter_name(self):
		"""Get the full name of the deleter, or if they don't have one, just return the author object itself (which will render as the author's username)"""
		name = self.deleter.get_full_name()

		if name:
			return name
		else:
			return self.deleter

	def __unicode__(self):
		return "Note by %s on %s %d", (author.get_full_name(), self.get_entity_name(), entity_id)
