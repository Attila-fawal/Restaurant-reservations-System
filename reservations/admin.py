from django.contrib import admin
from .models import Customer, Table, Reservation, Menu, Item, ReservationTable  

class ReservationTableInline(admin.TabularInline):  
    model = ReservationTable
    extra = 1  

class ReservationAdmin(admin.ModelAdmin):
    inlines = (ReservationTableInline,)
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
        "email"
    )
    display = "Customer Admin"

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Table)
admin.site.register(Reservation, ReservationAdmin)  
admin.site.register(Menu)  
admin.site.register(Item)  
