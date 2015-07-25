import datetime

from decorators import staff_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from models import Note
from forms import NoteForm

@staff_required
def new(request):
	#TODO: Replace this and similar instances with @require_POST decorator
	if not request.method == "POST":
		return HttpResponse(status=405)

	form = NoteForm(request.POST)
	if form.is_valid():
		note = form.save(commit=False)
		note.author = request.user
		note.save()
		messages.info(request, "Your note has been added.")

	return HttpResponseRedirect(request.POST['next'])

@staff_required
def delete(request):
	if not request.method == "POST":
		return HttpResponse(status=405)

	note_id = request.POST["note_id"]

	note = Note.objects.get(pk=note_id)
	note.message = "This note was deleted."
	note.date_deleted = datetime.datetime.now()
	note.deleter = request.user
	note.save()

	messages.info(request, "The note has been deleted.")

	return HttpResponseRedirect(request.POST['next'])
