from lxml.html.clean import clean_html

from django.db import models

from django.contrib.auth.models import User
from django.template import RequestContext
from django.template.loader import render_to_string

import settings

from positions.models import Organisation

# Create your models here.
class Mailout(models.Model):
	subject = models.CharField(max_length=127)
	body = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	sent = models.DateTimeField(blank=True, null=True)

	organisation = models.ForeignKey(Organisation, blank=True, null=True)
	created_by = models.ForeignKey(User, blank=True, null=True, related_name="mailouts_created")
	sent_by = models.ForeignKey(User, blank=True, null=True, related_name="mailouts_sent")

	class Meta:
		ordering = ['-created']

	@models.permalink
	def get_absolute_url(self):
		return ('mailer.views.mailout', (self.id,))

	def full_subject(self):
		if self.organisation:
			return "[%s] %s" % (self.organisation, self.subject)
		else:
			return "[%s] %s" % (settings.FRIENDLY_NAME, self.subject)

	def full_body(self):
		signature = render_to_string('layout/signature.txt', {})
		return """
		%s

		<span style="color: #666">%s</span>
		""" % (clean_html(self.body), signature.replace('\n', '<br/>\n'))

class Recipient(models.Model):
	mailout = models.ForeignKey(Mailout)
	user = models.ForeignKey(User)
	sent = models.DateTimeField(null=True)
	bounced = models.DateTimeField(null=True)
	memo = models.TextField(null=True, blank=True)
