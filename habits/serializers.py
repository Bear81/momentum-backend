from rest_framework import serializers
from .models import Habit, HabitLog

class HabitSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Habit
        fields = ["id", "owner", "name", "description", "period", "target", "tags",
                  "created_at", "updated_at"]

    def validate_target(self, value):
        if value < 1:
            raise serializers.ValidationError("Target must be at least 1.")
        return value


class HabitLogSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    habit_name = serializers.ReadOnlyField(source="habit.name")

    class Meta:
        model = HabitLog
        fields = ["id", "owner", "habit", "habit_name", "count", "noted_at", "note", "created_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        habit = attrs.get("habit") or getattr(self.instance, "habit", None)
        if request and request.user.is_authenticated and habit and habit.owner != request.user:
            raise serializers.ValidationError("You cannot log for a habit you do not own.")
        return attrs

    def validate_count(self, value):
        if value < 1:
            raise serializers.ValidationError("Count must be at least 1.")
        return value
