from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High")
    ]
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("LOCKED", "Locked")
    ]

    title = models.CharField(max_length=255)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES
    )
    estimated_time = models.IntegerField(
        help_text="Estimated completion time in minutes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    locked_until = models.DateTimeField(
        null=True,
        blank=True
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.priority}) - {self.status}"
