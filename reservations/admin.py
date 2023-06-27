from django.contrib import admin
from .models import Customer, Table, Reservation, Menu, Item  


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email"
    )
    display = "Customer Admin"

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Menu)  
admin.site.register(Item)  
