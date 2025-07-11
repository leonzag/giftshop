from django.urls import include, path

from . import views

app_name = "account"

urlpatterns = [
    # Встроенные URL-адреса аутентификации Django
    # Это включает login/, logout/, password_change/, password_reset/ и т.д.
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
]
