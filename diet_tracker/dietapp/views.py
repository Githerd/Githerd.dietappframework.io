from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('<h1>dietapp home</h1>')

def dashboard(request):
    return HttpResponse('<h1>dietapp dashboard</h1>')

def about(request):
    return HttpResponse('<h1>dietapp about</h1>')

def contact(request):
    return HttpResponse('<h1>dietapp contact</h1>')