from django.contrib import admin
from .models import Table, Transaction, Category

admin.site.register(Category)

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name",)
    list_filter = ("user",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "currency", "date", "table")
    search_fields = ("name", "table__name")
    list_filter = ("currency", "date")
    ordering = ("-date",)


