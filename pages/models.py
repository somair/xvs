from django.db import models

def link_position_choices():
	return (
		('header', 'Header'),
		('footer,', 'Footer'),
	)

class Link(models.Model):
	title = models.CharField(max_length=100)
	href = models.URLField(max_length=400)
	location = models.CharField(max_length=30, choices=link_position_choices(), default='header')


	def __unicode__(self):
		return self.title

	def render(self):
		return '<a href="%s">%s</a>' % (self.href, self.title)