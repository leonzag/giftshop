from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from cart.cart import Cart

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
            phone_number=cd["phone_number"],
        )
        if cart.coupon is not None:
            fields["coupon"] = cart.coupon
            fields["discount"] = cart.coupon.discount

        if request.user.is_authenticated:
            fields["user"] = request.user

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


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        "admin/orders/order/detail.html",
        {"order": order},
    )


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(
        request,
        "orders/order/detail.html",
        {"order": order}
    )


@login_required
def order_history(request):
    """
    Заказы текщего аутентифицированного пользователя
    """
    orders = request.user.orders.all()
    return render(
        request,
        "orders/order/history.html",
        {"orders": orders}
    )
