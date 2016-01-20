from django.db import models

class Link(models.Model):
	title = models.CharField(max_length=100)
	href = models.URLField(max_length=400)

	def __unicode__(self):
		return self.title

	def render(self):
		return '<a href="%s">%s</a>' % (self.href, self.title)