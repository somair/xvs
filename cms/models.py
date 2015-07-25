from django.db import models

class Page(models.Model):
	page_name = models.CharField(max_length=100)
	page_content = models.TextField()
	order = models.IntegerField()
	status = models.IntegerField()

	def __unicode__(self):
		return self.page_name