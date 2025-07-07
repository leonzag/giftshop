import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import Order, OrderItem


@admin.action(description="Export to CSV")
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={opts.verbose_name_plural}.csv"

    writer = csv.writer(response)

    exclude_fields = ["id"]
    header = []
    for f in opts.fields:
        if f.name not in exclude_fields:
            header.append(f.verbose_name or f.name)

    header_extra = ["Стоимость (без скидки)", "Стоимость (со скидкой)"]

    writer.writerow(header + header_extra)

    # Записываем данные для каждой строки (заказа)
    for obj in queryset:
        data_row = []
        for field in opts.fields:
            if field.name in exclude_fields:
                continue

            value = getattr(obj, field.name)

            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")

            elif field.name == "coupon":
                value = obj.coupon.code if obj.coupon else ""

            elif field.name == "discount":
                value = obj.discount

            else:
                value = str(value)

            data_row.append(value)

        data_row.append(obj.get_total_cost_without_discount())
        data_row.append(obj.get_total_cost())

        writer.writerow(data_row)

    return response


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]  # Позволяет искать продукт по ID, а не по выпадающему списку


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "city",
        "address",
        "postal_code",
        "paid",
        "created",
        "updated",
    ]
    list_filter = ["paid", "created", "updated"]
    search_fields = ["first_name", "last_name", "email", "address"]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
