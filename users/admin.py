from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User, Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'team', 'is_admin', 'date_joined']
    list_filter = ['is_admin', 'team', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('is_admin', 'team')
        }),
    )