from django.http import HttpResponse
from django.http import HttpRequest

def hello_world(request):
    return HttpResponse("Hello world!")
