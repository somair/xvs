
import settings

def instance_dictionary():
	"""A dictionary with values specific to the instance,
	which are used to customise outbound emails."""
	return {
		'FRIENDLY_NAME': settings.FRIENDLY_NAME,
		'SUPPORT_EMAIL': settings.SUPPORT_EMAIL,
	}
	