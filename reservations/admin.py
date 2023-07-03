from django.contrib import admin
from .models import Customer, Table, Reservation, Menu, Item


class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "time",
        "guests",
        "customer_user",
        "name",
        "email",
        "phone_number",
        "get_tables",
    )

    def get_tables(self, obj):
        return ", ".join([str(table.id) for table in obj.tables.all()])
    get_tables.short_description = 'Table IDs'


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "user_email",
    )
    display = "Customer Admin"

    def get_queryset(self, request):
        return super(CustomerAdmin, self).get_queryset(
            request).select_related('user')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'


class TableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "number",
        "capacity",
        "is_reserved",
    )

    def is_reserved(self, obj):
        return obj.is_reserved
    is_reserved.short_description = 'Is Reserved'
    is_reserved.boolean = True


class MenuAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    display = "Menu Admin"


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "menu",
    )
    display = "Item Admin"


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Item, ItemAdmin)
