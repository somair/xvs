import json

from django.http import HttpResponse

def JsonResponse(data):
    return HttpResponse(json.dumps(data), mimetype="application/json")

class exception_to_json_error(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, request, *args, **kwargs):
        try:
            return self.f(request, *args, **kwargs)
        except Exception, e:
            return JsonResponse({"error": e.message})
    
