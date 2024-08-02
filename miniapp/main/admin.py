from django.contrib import admin
from .models import User, GlobalTask, Referral

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'username', 'nickname', 'points', 'referral_code')
    search_fields = ('telegram_id', 'username', 'nickname')
    list_filter = ('points',)

@admin.register(GlobalTask)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'task_image', 'points')
    search_fields = ('task_name', 'task_description')

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'referred_user')
    search_fields = ('user__username', 'referred_user__username')
