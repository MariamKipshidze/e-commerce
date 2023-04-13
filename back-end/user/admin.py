from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'company_name']
    search_fields = ['email']
