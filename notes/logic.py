


from django.core.urlresolvers import reverse
from decorators import staff_required
from models import Note, ENTITIES




@staff_required
def get_notes(request, entity, redirect=None):
	"""A macro for getting notes, except that it only returns actual data
	if the user is a staff member."""

	entity_type = get_entity_type_num(entity)

	notes = []
	notes_not_deleted = []
	post_url = ""

	# Only fetch notes if the user is a staff member.
	if request.user.is_staff:
		notes = Note.objects.filter(entity_id=entity.id, entity_type=entity_type)
		notes_not_deleted = notes.filter(deleter__isnull=True)
		post_url = reverse('notes.views.new')
		delete_url = reverse('notes.views.delete')

	return {
		"notes": notes,
		"notes_not_deleted": notes_not_deleted,
		"redirect": redirect if redirect else entity.get_absolute_url(),
		"entity_id": entity.id,
		"entity_type": entity_type,
		"post_url": post_url,
		"delete_url": delete_url,
	}

def get_entity_type_num(entity):
	for (num, clazz) in ENTITIES:
		if isinstance(entity, clazz):
			return num
