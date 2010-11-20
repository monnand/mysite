from django.http import HttpResponse
from django.http import HttpRequest

def hello_world(request):
    return HttpResponse("Hello world!")

def read_header(request):
    header = request.META['HTTP_HOST']
    agent = request.META['HTTP_USER_AGENT']
    host = request.META['REMOTE_ADDR']
    return HttpResponse(host)

