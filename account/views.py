from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import UserRegistrationForm


def register(request):
    if request.method != "POST":
        user_form = UserRegistrationForm()
        return render(request, "account/register.html", {"user_form": user_form})

    user_form = UserRegistrationForm(request.POST)

    if not user_form.is_valid():
        return render(request, "account/register.html", {"user_form": user_form})

    new_user = user_form.save(commit=False)
    new_user.set_password(user_form.cleaned_data["password"])
    new_user.save()
    login(request, new_user)

    return render(request, "account/register_done.html", {"new_user": new_user})
