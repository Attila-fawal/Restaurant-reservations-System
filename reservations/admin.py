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
    )


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        'phone_number',
    )
    display = "Customer Admin"


class TableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "capacity"
        
    )
    display = "Table Admin"


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
