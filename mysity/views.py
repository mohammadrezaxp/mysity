from  django.http import HttpResponse , JsonResponse
from django.shortcuts import render


def about (request):
   return render(request,'indx.html')
def contact(request) :
    return render(request,'about.html')