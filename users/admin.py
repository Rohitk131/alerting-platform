from django.contrib import admin
from .models import Team, User

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass