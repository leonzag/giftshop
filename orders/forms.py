from django import forms

CLASS_ATTR = "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"


class OrderCreateForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"class": CLASS_ATTR}),
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"class": CLASS_ATTR}),
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": CLASS_ATTR}))
    address = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={"class": CLASS_ATTR}),
    )
    postal_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": CLASS_ATTR}),
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": CLASS_ATTR}),
    )
