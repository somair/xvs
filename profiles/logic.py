


def get_action_ids(request):
	return [int(idstr) for idstr in request.REQUEST['action_ids'].split(",")]