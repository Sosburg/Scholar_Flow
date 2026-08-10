from django.contrib.auth.models import User
from django.db import models

class Workspace(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="workspace")
    name = models.CharField(max_length=120, default="My Research Workspace")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username} workspace"

class Theme(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="themes")
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=20, default="#3b82f6")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("workspace", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name

class Paper(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="papers")
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    year = models.CharField(max_length=10, blank=True)
    pdf = models.FileField(upload_to="papers/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title

class Statement(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="statements")
    text = models.TextField()
    page_number = models.PositiveIntegerField(default=1)
    note = models.TextField(blank=True)
    themes = models.ManyToManyField(Theme, blank=True, related_name="statements")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text[:80]
