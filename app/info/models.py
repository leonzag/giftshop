from django.db import models


class ContactMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"

    def __str__(self):
        return f"Сообщение от {self.name} ({self.email})"
