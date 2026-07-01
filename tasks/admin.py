from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'created_at', 'locked_until')
    list_filter = ('status', 'priority')
    search_fields = ('title',)
