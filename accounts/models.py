from django.db import models

# Create your models here.

class PlateRecord(models.Model):
    # your fields here
    pass

class Plate(models.Model):
    plate_number = models.CharField(max_length=20)
    vehicle = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    feedback = models.TextField()

    def __str__(self):
        return self.plate_number

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
