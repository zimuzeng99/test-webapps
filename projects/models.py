from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    type = models.CharField(max_length=100)
    duration = models.FloatField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.project.title

class CompletedProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.project.title
