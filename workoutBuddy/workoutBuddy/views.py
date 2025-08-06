from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings



def HomePage(request):
    return render(request, 'mainPage/home.html')

def AboutPage(request):
    return render(request,'mainPage/about.html' )

def contactPage(request):
    return render(request,'mainPage/contact_us_2.html' )