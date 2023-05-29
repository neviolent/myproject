from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count

def index(request):
    return render(request, './resources/templates/index.html')

def about(request):
    return render(request, './resources/templates/about.html')

