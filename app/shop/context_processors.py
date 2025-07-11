from .models import Category


def categories(_):
    return {
        "categories": Category.objects.all(),
    }
