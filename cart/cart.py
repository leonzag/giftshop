from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session_id = settings.CART_SESSION_ID
        self.session = request.session

        cart = self.session.get(self.session_id)
        if not cart:
            cart = self.session[self.session_id] = {}

        self.cart = cart

    def save(self):
        # Пометить сессию как "измененную", чтобы убедиться, что она сохранена
        self.session.modified = True

    def add(self, product: Product, quantity=1, override_quantity=False):
        """
        Добавить товар в корзину или обновить его количество.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def remove(self, product: Product):
        """
        Удалить товар из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получить объекты Product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()  # Создаем копию корзины, чтобы избежать изменения во время итерации
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Подсчитать все товары в корзине.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчитать общую стоимость товаров в корзине.
        """
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        """
        Удалить корзину из сессии.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
