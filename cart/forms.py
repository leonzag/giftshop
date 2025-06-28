from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=0,
        max_value=20,
        widget=forms.NumberInput(
            attrs={
                "inputmode": "numeric",
                "oninput": r"this.value = this.value.replace(/\D+/g, '')",
            }
        ),
        label="Quantity",
        initial=1,
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
