from django.shortcuts import render

from .forms import ContactForm
from .models import ContactMessage
from .settings import CONTACT_EMAIL
from .tasks import send_contact_email


def info(request):
    form = ContactForm()
    if request.method != "POST":
        return render(request, "info/info.html", {"form": form})

    form = ContactForm(request.POST)
    if not form.is_valid():
        form = ContactForm()
        return render(request, "info/info.html", {"form": form})

    contact_message = ContactMessage.objects.create(
        name=form.cleaned_data["name"],
        email=form.cleaned_data["email"],
        message=form.cleaned_data["message"],
    )
    send_contact_email.delay(
        contact_message.id,
        CONTACT_EMAIL,
    )

    return render(request, "info/contact_success.html")
