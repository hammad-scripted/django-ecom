from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import UserRegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("product_list")

    form = UserRegisterForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        authenticated_user = authenticate(
            request,
            username=user.get_username(),
            password=form.cleaned_data["password1"],
        )
        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, "Your account is ready. Welcome to ShopHub!")
            return redirect("product_list")
        messages.success(request, "Your account is ready. Sign in to continue.")
        return redirect("login")

    return render(request, "users/signup.html", {"form": form})


@require_POST
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been signed out.")
    return redirect("product_list")
