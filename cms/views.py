from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from cms.forms import WebsiteForm
from cms.models import Page
from decorators import staff_required
from django.template import RequestContext

# CMS Admin Page.
@staff_required
def siteadmin(request):
	pages = Page.objects.order_by('order')
	return render_to_response("cms/admin.html",
		{"pages": pages}, 
		context_instance=RequestContext(request))

# Publist and unpublish stuff!
@staff_required
def publish(request, pageid):
	page = Page.objects.get(pk=pageid)
	if page.status == 1:
		# Unpublish
		page.status = 0
		page.save()
	elif page.status == 0:
		# Publish
		page.status = 1
		page.save()
	return HttpResponseRedirect('/site/admin/')


# Re-order: DOWN!
@staff_required
def down(request, current_order, new_order):
	first_page = Page.objects.get(order=current_order)
	second_page = Page.objects.get(order=new_order)

	first_page.order = new_order
	first_page.save()
	second_page.order = current_order
	second_page.save()

	return HttpResponseRedirect('/cms/order/')

# Re-order: UP!
@staff_required
def up(request, current_order, new_order):
	first_page = Page.objects.get(order=current_order)
	second_page = Page.objects.get(order=new_order)

	first_page.order = new_order
	first_page.save()
	second_page.order = current_order
	second_page.save()

	return HttpResponseRedirect('/cms/order/')

# Re-order pages.
@staff_required
def order(request):
	pages = Page.objects.order_by('order')
	page_list=[]
	order_links=[]
	order_links_reverse=[]
	for page in pages:
		page_list.append(page.order)

	list_length = len(page_list)

	for i in xrange(len(page_list)):
		current_page = page_list[i]
		previous_page = page_list[i-1]
		output = "%d/%d" % (current_page, previous_page)
		order_links.append(output)

		if i+1 < list_length:
			page_before = page_list[i+1]
			output2 = "%d/%d" % (current_page, page_before)
			order_links_reverse.append(output2)
		else:
			page_before = page_list[0]
			output2 = "%d/%d" % (current_page, page_before)
			order_links_reverse.append(output2)

	return render_to_response("cms/order.html",
		{
			"pages": pages,
			"order_links": order_links,
			"order_links_reverse": order_links_reverse,
		},
		context_instance=RequestContext(request))

# Delete pages :(
@staff_required
def delete(request, offset):
	if request.method == 'POST':
		page = Page.objects.get(pk=offset)
		page.delete()
		redirect = '/site/admin/'
		return HttpResponseRedirect(redirect)
	else:
		page = Page.objects.get(pk=offset)
		return render_to_response("cms/delete.html", {
				"page": page
			}, 
			context_instance=RequestContext(request))

# Edit them here!
@staff_required
def edit(request, offset):
	offset = get_object_or_404(Page, pk=offset)
	if request.method == 'POST':
		form = WebsiteForm(request.POST, instance=offset)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/site/admin')
	else:
		form = WebsiteForm(instance=offset)

	return render_to_response("cms/cms.html", {'form': form}, 
		context_instance=RequestContext(request))

# Create pages here.
@staff_required
def cms(request):
	if request.method == 'POST':
		form = WebsiteForm(request.POST)
		if form.is_valid():
			newpage = form.save(commit=False)
			newpage.order = order_for_last_page()
			newpage.save()

			return HttpResponseRedirect('/site/admin')
	else:
		form = WebsiteForm()
	return render_to_response("cms/cms.html", 
		{ "form": form }, 
		context_instance=RequestContext(request))

# CMS preview page, will be for admins only.
@staff_required
def pages(request):
	pages = Page.objects.all()
	return render_to_response('cms/pages.html', {'pages' : pages,}, 
		context_instance=RequestContext(request))

@staff_required
def pageview(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	pageview = Page.objects.get(pk=offset)
	pages = Page.objects.all().order_by('order')
	return render_to_response('cms/preview.html', 
		{
			"pageview": pageview,
			"pages": pages,
		}, 
		context_instance=RequestContext(request))

#####
# PUBLIC VIEWS BELOW
#####

# This is the front page.
def site(request):
	pages = Page.objects.filter(status=1).order_by('order')

	# If there aren't any pages in the CMS, display a nice message.
	if not len(pages):
		return render_to_response('layout/message.html', 
			{ "message": "The CMS doesn't contain any published pages!" }, 
			context_instance=RequestContext(request))

	page = pages[0]
	return render_to_response('cms/sitehome.html', 
		{
			"pages": pages,
			"page": page,
		},
		context_instance=RequestContext(request))

# Individual pages.
def siteview(request, offset):
	try:
		pageview = Page.objects.get(pk=offset)
	except Page.DoesNotExist:
		raise Http404()

	if pageview.status == 1:
		published_pages = Page.objects.filter(status=1).order_by('order')
		return render_to_response('cms/sitehome.html', 
			{
				"pages": published_pages,
				"page": pageview,
			}, 
			context_instance=RequestContext(request))
	else:
		raise Http404()


def order_for_last_page():
	"""Returns the order of the last page plus one, such that any page
	with the new order number will be the last page in the navigation
	list."""
	pages = Page.objects.all()

	if Page.objects.count():
		return pages.order_by('-order')[0].order + 1
	else:
		return 0




