from django.db import models

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=100,blank=False)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True,blank=True)
    priority = models.CharField(
        max_length=10,
        choices=[("HIGH", "High"), ("MEDIUM", "Medium"), ("LOW", "Low")],
        default="MEDIUM"
    )
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        due = self.due_date.isoformat() if self.due_date else "No due"
        return f"{self.title} ({due})"
