from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Код купона")
    valid_from = models.DateTimeField(verbose_name="Действителен с")
    valid_to = models.DateTimeField(verbose_name="Действителен до")
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Скидка (%)")
    active = models.BooleanField(default=False, verbose_name="Активен")

    class Meta:
        ordering = ["-valid_from"]
        verbose_name = "Купон"
        verbose_name_plural = "Купоны"

    def __str__(self):
        return self.code
