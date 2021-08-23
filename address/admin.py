from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Address


class AddressInline(admin.StackedInline):
    model = Address


class UserAdmin(BaseUserAdmin):
    inlines = (AddressInline,)


admin.site.register(User, UserAdmin)
