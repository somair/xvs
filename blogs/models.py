import datetime

from django.db import models
from django.contrib.auth.models import User

from lxml.html.clean import clean_html

PUBLISHED = 1

STATUS_CHOICES = ((0, 'Draft'),
		          (PUBLISHED, 'Published'))



class Entry(models.Model):
	title = models.CharField(max_length=120)
	body = models.TextField()
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)
	published = models.DateTimeField(auto_now_add=True)
	publisher = models.ForeignKey(User)

	def clean_body(self):
		return clean_html(self.body) 

	@models.permalink
	def get_absolute_url(self):
		return ('blogs.views.entryview', (self.publisher.id, self.id,))

	class Meta:
		verbose_name_plural = "entries"

	def __unicode__(self):
		return self.title