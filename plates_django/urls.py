from django.contrib import admin
from django.urls import path
#from .views import upload_csv
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard URL
    path('', views.index_view, name='index'),  # Root URL (empty path)
    path ('platerecords/' , views.platerecords_view, name='platerecords'),
    path ('super/' , views.super_view, name='super'),
    path ('logout/' , views.logout_view, name='logout'),
    path('plateaction/', views.plate_view, name='plateaction'),
    path('userpage/', views.userpage_view, name='userpage'),
    #path('import_xml/', views.import_xml, name='import_xml'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('import_file/', views.import_file, name='import_file'),
    ##path('upload-csv/', upload_csv, name='upload_csv'),
]
