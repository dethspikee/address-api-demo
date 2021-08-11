from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Address


#admin.site.register(User, UserAdmin)
#admin.site.register(Address)


class AddressInline(admin.TabularInline):
    model = Address


class UserAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Address)
