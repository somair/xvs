from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from work_experience import models, forms

@login_required
def new(request):

	print request

	template = 'work_experience/new.html'

	context = {

	}

	return render(request, template, context)



