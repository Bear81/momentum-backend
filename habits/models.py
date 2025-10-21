from django.conf import settings
from django.db import models

class Habit(models.Model):
    PERIOD_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    period = models.CharField(max_length=16, choices=PERIOD_CHOICES, default="daily")
    target = models.PositiveIntegerField(default=1, help_text="Target count per period")
    tags = models.CharField(max_length=120, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("owner", "name")

    def __str__(self):
        return f"{self.name} ({self.owner})"


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habit_logs")
    count = models.PositiveIntegerField(default=1)
    noted_at = models.DateField()
    note = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-noted_at", "-created_at"]
        unique_together = ("habit", "owner", "noted_at")

    def __str__(self):
        return f"{self.habit.name} x{self.count} on {self.noted_at}"
