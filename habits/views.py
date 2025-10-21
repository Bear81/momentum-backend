from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import HabitFilter, HabitLogFilter

class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = HabitFilter
    search_fields = ["name", "description", "tags"]
    ordering_fields = ["created_at", "updated_at", "name"]

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Habit.objects.all()


class HabitLogListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = HabitLogFilter
    search_fields = ["note", "habit__name"]
    ordering_fields = ["noted_at", "created_at", "count"]

    def get_queryset(self):
        return HabitLog.objects.filter(owner=self.request.user).select_related("habit")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HabitLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitLogSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return HabitLog.objects.select_related("habit")
