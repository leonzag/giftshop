from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at", "message_snippet"]
    list_filter = ["created_at"]
    search_fields = ["name", "email", "message"]
    date_hierarchy = "created_at"
    readonly_fields = ["name", "email", "message", "created_at"]

    @admin.display(ordering="message_snippet", description="Сообщение")
    def message_snippet(self, obj):
        """Отображает сокращенный текст сообщения в списке."""
        if len(obj.message) > 75:
            return obj.message[:75] + "..."
        return obj.message

    def has_add_permission(self, request):
        """Запрещает добавление новых сообщений через админку."""
        return False

    def has_change_permission(self, request, obj=None):
        """Запрещает изменение сообщений через админку."""
        return False
