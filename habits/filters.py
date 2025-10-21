import django_filters
from .models import Habit, HabitLog

class HabitFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name="tags", lookup_expr="icontains")
    period = django_filters.CharFilter(field_name="period", lookup_expr="iexact")
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")

    class Meta:
        model = Habit
        fields = ["tag", "period", "created_before", "created_after"]


class HabitLogFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="noted_at", lookup_expr="exact")
    date_from = django_filters.DateFilter(field_name="noted_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="noted_at", lookup_expr="lte")

    class Meta:
        model = HabitLog
        fields = ["date", "date_from", "date_to", "habit"]
