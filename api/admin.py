from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User 

class CustomUserAdmin(UserAdmin):
    """
    Customises the admin panel in django for the user model,and ensures to add additional infor such as the 'dob' and hobbies into the admin interface
    """
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("dob", "hobbies")
        }),
    )

admin.site.register(User, CustomUserAdmin)
