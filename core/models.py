from django.db import models

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    schedule_html = models.TextField()
    occupied_classrooms = models.TextField()

    def __str__(self):
        return self.name
