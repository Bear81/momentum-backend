from django.urls import path
from .views import (
    HabitListCreateView, HabitDetailView,
    HabitLogListCreateView, HabitLogDetailView
)

urlpatterns = [
    path("habits/", HabitListCreateView.as_view(), name="habit-list-create"),
    path("habits/<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
    path("logs/", HabitLogListCreateView.as_view(), name="habitlog-list-create"),
    path("logs/<int:pk>/", HabitLogDetailView.as_view(), name="habitlog-detail"),
]
