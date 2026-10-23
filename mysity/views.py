from django.contrib import messages
from django.shortcuts import redirect, render

from blog.visibility import visible_posts
from mysity.forms import Contactform, newsform


def home(request):
    posts = visible_posts(request.user).order_by("-published_date")[:3]
    context = {"posts": posts}
    return render(request, "mysity/index.html", context)


def contact(request):
    if request.method == "POST":
        form = Contactform(request.POST)
        if form.is_valid():
            contacts = form.save(commit=False)
            contacts.save()
            messages.add_message(request, messages.SUCCESS, "Your ticket is successful")
            return redirect("contact")
        else:
            messages.add_message(
                request, messages.ERROR, "Your ticket is NOT successful"
            )
    else:
        form = Contactform()

    context = {"form": form}
    return render(request, "mysity/contact.html", context)


def about(request):
    return render(request, "mysity/about.html")


def news(request):
    if request.method == "POST":
        form = newsform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have subscribed successfully.")
            return redirect("index")
    else:
        form = newsform()

    context = {"form": form}
    return render(request, "mysity/contact.html", context)
