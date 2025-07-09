from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from coupons.models import Coupon
from shop.models import Product


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        Coupon,
        related_name="orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Купон",
    )
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Скидка (%)"
    )

    class Meta:
        ordering = ["-created"]  # Сортировка по убыванию даты создания
        indexes = [
            models.Index(fields=["-created"]),  # Индекс для поля created
        ]

    def __str__(self):
        return f"Order {self.id}"

    def get_discount_cost(self):
        """
        Стоимость скидки
        """
        if self.discount:
            return (self.discount / Decimal(100)) * self.get_total_cost_without_discount()
        return Decimal(0)

    def get_total_cost_without_discount(self):
        """
        Стоимость заказа БЕЗ учёта скидок
        """
        return sum(item.get_cost() for item in self.items.all())

    def get_total_cost(self):
        """
        Cтоимость заказа с учётом скидок
        """
        return self.get_total_cost_without_discount() - self.get_discount_cost()


class OrderItem(models.Model):
    """Позиция заказа

    Attributes:
        order: родительский заказ
        product: товарное наименование
        price: цена товарного наименования
        quantity: колчество товаров
    """

    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
