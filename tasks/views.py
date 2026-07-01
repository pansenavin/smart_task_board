from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Task
from .serializers import TaskSerializer

class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        two_minutes_ago = timezone.now() - timedelta(minutes=2)
        recent_tasks_count = Task.objects.filter(created_at__gte=two_minutes_ago).count()
        
        status_val = "PENDING"
        locked_until = None
        
        if recent_tasks_count >= 3:
            status_val = "LOCKED"
            locked_until = timezone.now() + timedelta(minutes=5)
            
        task = Task.objects.create(
            **data,
            status=status_val,
            locked_until=locked_until
        )
        serializer.instance = task

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskCompleteView(APIView):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        
        if task.status == "LOCKED" and task.locked_until and task.locked_until > timezone.now():
            return Response({"success": False, "hint": "The board asks for patience."}, status=status.HTTP_400_BAD_REQUEST)
            
        if task.status == "LOCKED" and task.locked_until and task.locked_until <= timezone.now():
            task.status = "PENDING"
            task.locked_until = None
            task.save(update_fields=['status', 'locked_until'])

        if task.status == "COMPLETED":
            return Response({"success": False, "hint": "The deed is already done."}, status=status.HTTP_400_BAD_REQUEST)

        if task.id % 5 == 0:
            return Response({"success": False, "hint": "Not all doors open on the first attempt."}, status=status.HTTP_400_BAD_REQUEST)

        if task.priority == "HIGH":
            if not Task.objects.filter(priority="LOW", status="COMPLETED").exists():
                return Response({"success": False, "hint": "Something simpler still waits in the shadows."}, status=status.HTTP_400_BAD_REQUEST)

        created_minute = task.created_at.minute
        if created_minute % 2 == 0:
            deadline = task.created_at + timedelta(minutes=task.estimated_time)
            if timezone.now() > deadline:
                return Response({"success": False, "hint": "The clock disagrees with your ambition."}, status=status.HTTP_400_BAD_REQUEST)

        task.status = "COMPLETED"
        task.completed_at = timezone.now()
        task.save(update_fields=['status', 'completed_at'])
        
        return Response({"success": True, "message": "Task completed successfully"}, status=status.HTTP_200_OK)

def task_board_ui(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/index.html', {'tasks': tasks})

