from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),  # URL for uploading CSV
    # You can add more paths for other views like generating codes and exporting CSV
]
