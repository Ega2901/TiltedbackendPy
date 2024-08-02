# file: myapp/admin.py
from django.contrib import admin
from .models import User, Task

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'tg_username', 'nickname', 'points', 'referral_code', 'referrer')
    search_fields = ('telegram_id', 'tg_username', 'nickname')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'completed', 'user', 'task_url', 'points')
    search_fields = ('name', 'user__nickname')
