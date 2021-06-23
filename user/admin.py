from django.contrib import admin
from .models import Usert

# Register your models here.


class UsertAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")


admin.site.register(Usert, UsertAdmin)
