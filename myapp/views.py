from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world!")

def about(request):
    return HttpResponse("<h1>Welcome to my about page!</h1>")