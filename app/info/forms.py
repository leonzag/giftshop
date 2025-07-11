from django import forms

CLASS_ATTR = "block w-full rounded-md bg-white px-3 py-2 text-base text-gray-900 shadow-sm outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": CLASS_ATTR,
                "placeholder": "Как вас зовут?",
            }
        ),
        label="Ваше имя",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": CLASS_ATTR,
                "placeholder": "your@email.com",
            }
        ),
        label="Ваш Email",
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": CLASS_ATTR,
                "placeholder": "Введите ваше сообщение здесь...",
            }
        ),
        label="Сообщение",
    )
