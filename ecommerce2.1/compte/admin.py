from django.contrib import admin
from compte.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "username", 'last_name', "email", "is_active", "is_staff", "pays"]
    ordering = ["first_name"]
    list_filter = ['pays']
    search_fields = ["first_name"]

admin.site.register(Client, ClientAdmin)