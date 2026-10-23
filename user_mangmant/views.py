from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST

from .forms import SignupForm


@require_http_methods(["GET", "POST"])
def loge_page(request):
    if request.user.is_authenticated:
        return redirect("index")
    form = AuthenticationForm(
        request, data=request.POST if request.method == "POST" else None
    )
    next_url = request.POST.get("next") or request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(
        next_url, {request.get_host()}, require_https=request.is_secure()
    ):
        next_url = reverse("index")
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        if not request.POST.get("remember"):
            request.session.set_expiry(0)
        messages.success(request, "Welcome back!")
        return redirect(next_url or "index")
    if request.method == "POST":
        messages.error(request, "Invalid username or password.")
    return render(
        request, "User_mage/login_user.html", {"form": form, "next": next_url}
    )


@require_POST
def logout_page(request):
    logout(request)
    messages.info(request, "You have signed out.")
    return redirect("User_manage:login")


@require_http_methods(["GET", "POST"])
def sing_up_page(request):
    if request.user.is_authenticated:
        return redirect("index")
    data = request.POST.copy() if request.method == "POST" else None
    if data is not None:
        data["password1"] = data.get("password", "")
        data["password2"] = data.get("password_confirm", "")
    form = SignupForm(data)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save()
        except IntegrityError:
            form.add_error("username", "This username is already registered.")
        else:
            login(request, user)
            messages.success(request, "Your account has been created.")
            return redirect("index")
    return render(request, "User_mage/index.html", {"form": form})
