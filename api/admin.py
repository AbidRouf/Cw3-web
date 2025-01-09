from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User 

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("dob", "hobbies")
        }),
    )

admin.site.register(User, CustomUserAdmin)
