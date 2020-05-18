from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# def home(request):
#     return HttpResponse("Project 3: TODO")


def home(request):
    return render(request, 'index.html')