from django.contrib import admin

from habit.models import Habit


@admin.register(Habit)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'action', 'is_public', 'owner')
