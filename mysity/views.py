from  django.http import HttpResponse , JsonResponse
from django.shortcuts import render


def home (request):
    return render(request, 'mysity/index.html')
def contact(request) :
    return render(request,'mysity/contact.html')
def about (request) :
    return render(request,'mysity/about.html')

def blog_home (request) :
    return render(request,'blog/blog-home.html')

def blog_single (request) :
    return render(request,'blog/blog-single.html')