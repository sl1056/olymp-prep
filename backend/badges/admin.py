# badges/admin.py
from django.contrib import admin
from .models import Badge, UserBadge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['icon', 'title', 'type', 'condition_subject', 'condition_min_solved', 'condition_min_correct_ratio']
    list_filter = ['type', 'condition_subject']
    search_fields = ['title', 'description']

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'status', 'earned_at']
    list_filter = ['status', 'badge__type', 'badge']
    search_fields = ['user__username', 'badge__title']