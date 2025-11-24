from blog.models import Post
from django.shortcuts import render, redirect
from mysity.forms import Contactform , newsform
from django.contrib import messages
def home (request):
    posts = Post.objects.filter(status=1).order_by('-published_date')[:3]
    context = {'posts':posts}
    return render(request, 'mysity/index.html',context)
def contact(request):
    if request.method == 'POST':
        form = Contactform(request.POST)
        if form.is_valid():
            contacts = form.save(commit=False)
            contacts.name = 'ناشناس'
            contacts.save()
            messages.add_message(request,messages.SUCCESS,'Your ticket is successful')
            return  redirect('contact')
        else:
            messages.add_message(request,messages.ERROR,'Your ticket is NOT successful')
    else:
        form = Contactform()

    context = {'form': form}
    return render(request, 'mysity/contact.html', context)

def about (request) :
    return render(request,'mysity/about.html')


def news(request):
    if request.method =='POST':
        form = newsform(request.POST)
        if form.is_valid():
            form.save()
    else:
        form=newsform()

    context ={'form':form}
    return render(request,'mysity/contact.html',context)
