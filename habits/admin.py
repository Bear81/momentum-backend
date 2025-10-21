from django.contrib import admin
from .models import Habit, HabitLog

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "name", "period", "target", "created_at")
    search_fields = ("name", "tags", "owner__username")
    list_filter = ("period",)

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ("id", "habit", "owner", "count", "noted_at", "created_at")
    search_fields = ("habit__name", "owner__username", "note")
    list_filter = ("noted_at",)
