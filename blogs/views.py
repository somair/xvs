from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from blogs.forms import blog_form
from blogs.models import Entry
from django.contrib.auth.models import User
from decorators import staff_required
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import settings


def throw_404_unless_allowed(blogger):
	"""Throw a HTTP 404 response if the blogger
	is not allowed to blog in this configuration."""

	if blogger.is_staff and settings.FEATURE_SITE_BLOG:
		# Staff members are allowed to blog when there is a site blog.
		return

	if blogger.get_profile().is_volunteer and settings.FEATURE_VOLUNTEER_BLOGS:
		# Volunteers are allowed to blog when volunteer blogs are enabled.
		return

	if blogger.get_profile().is_representative and settings.FEATURE_ORGANISATION_BLOGS:
		# Representatives are allowed to blog when org blogs are enabled.
		return

	# This person is not allowed to blog, or a blog should not be accessible
	# for this person.
	raise Http404


# View list of users who have made a blog post.
@login_required
def bloggers(request):
	entries = Entry.objects.all()

	bloggers = set([e.publisher for e in entries])

	return render_to_response("blog/bloggers.html",
		{"bloggers": bloggers},
		context_instance=RequestContext(request))

def myblog(request):
	entries = Entry.objects.filter(publisher=request.user.id).exclude(status=0).order_by('-published')
	blogger = User.objects.get(pk=request.user.id)

	throw_404_unless_allowed(blogger)

	return render_to_response("blog/blog.html",
		{"entries": entries,
		"blogger": blogger},
		context_instance=RequestContext(request))

@login_required
def blogview(request, user_id):
	if User.objects.filter(pk=user_id).count():
		entries = Entry.objects.filter(publisher=user_id).exclude(status=0).order_by('-published')
		blogger = User.objects.get(pk=user_id)

		throw_404_unless_allowed(blogger)

		return render_to_response("blog/blog.html",
			{"entries": entries,
			"blogger": blogger},
			context_instance=RequestContext(request))
	else:
		raise Http404


@login_required
def entryview(request, user_id, entry_id):
	entry = get_object_or_404(Entry, publisher=user_id, pk=entry_id)
	blogger = entry.publisher

	throw_404_unless_allowed(blogger)

	return render_to_response("blog/blog.html",
		{"entries": [entry],
		"blogger": blogger},
		context_instance=RequestContext(request))


# Add new blog entry.
@login_required
def newentry(request):
	throw_404_unless_allowed(request.user)

	if request.method == 'POST':
		form = blog_form(request.POST)
		if form.is_valid():
			Entry = form.save(commit=False)
			Entry.publisher = request.user
			Entry.save()
		return HttpResponseRedirect('/blogs/admin')
	else:
		form = blog_form()
	return render_to_response("blog/new_blog.html",
		{"form": form},
		context_instance=RequestContext(request))

# Edit a blog entry.
@login_required
def editentry(request, entry_id):
	throw_404_unless_allowed(request.user)

	the_entry = get_object_or_404(Entry, pk=entry_id, publisher=request.user)
	if request.method == 'POST':
		form = blog_form(request.POST, instance=the_entry)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/blogs/admin')
	else:
		form = blog_form(instance=the_entry)

	return render_to_response("blog/new_blog.html", {'form': form}, 
		context_instance=RequestContext(request))

# Delte a blog entry :(
@login_required
def deleteentry(request, entry_id):
	throw_404_unless_allowed(request.user)

	the_entry = get_object_or_404(Entry, pk=entry_id, publisher=request.user)
	if request.method == 'POST':
		the_entry.delete()
		return HttpResponseRedirect('/blogs/admin')
	else:
		redirect = '/blogs/'+str(request.user.pk)
		return render_to_response("blog/delete.html", {
				"page": the_entry,
				"redirect": redirect
			}, 
			context_instance=RequestContext(request))

@login_required
def blogadmin(request):
	throw_404_unless_allowed(request.user)

	entries = Entry.objects.filter(publisher=request.user.id).order_by('published')
	return render_to_response("blog/admin.html",
		{"pages": entries}, 
		context_instance=RequestContext(request))

@staff_required
def publishentry(request, entry_id):
	throw_404_unless_allowed(request.user)

	the_entry = get_object_or_404(Entry, pk=entry_id, publisher=request.user)
	if the_entry.status == 1:
		# Unpublish
		the_entry.status = 0
		the_entry.save()
	elif the_entry.status == 0:
		# Publish
		the_entry.status = 1
		the_entry.save()
	return HttpResponseRedirect('/blogs/admin')