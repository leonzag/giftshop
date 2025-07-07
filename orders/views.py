from django.shortcuts import redirect, render

from cart.cart import Cart
from shop.models import Product

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)  # Получаем текущую корзину пользователя
    form = OrderCreateForm()  # Пустая форма для GET-запроса

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if not form.is_valid():
            return render(request, "orders/order/create.html", {"cart": cart, "form": form})

        cd = form.cleaned_data
        fields = dict(
            first_name=cd["first_name"],
            last_name=cd["last_name"],
            email=cd["email"],
            address=cd["address"],
            postal_code=cd["postal_code"],
            city=cd["city"],
        )
        if cart.coupon is not None:
            fields["coupon"] = cart.coupon
            fields["discount"] = cart.coupon.discount

        order = Order.objects.create(**fields)

        for it in cart:
            OrderItem.objects.create(order=order, product=it["product"], price=it["price"], quantity=it["quantity"])

        cart.clear()  # Очищаем корзину после создания заказа

        order_created.delay(order.id)

        return render(
            request,
            "orders/order/created.html",  # Перенаправляем на страницу подтверждения
            {"order": order},
        )

    return render(
        request,
        "orders/order/create.html",  # Отображаем форму создания заказа
        {"cart": cart, "form": form},
    )
