from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render, get_object_or_404
import openpyxl
from .forms import ExcelUploadForm
from .models import PlateRecord, Plate, UploadedFile
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import pandas as pd
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'username': request.user.username})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"User {username} logged in successfully.")  # Debug log
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "account/login.html", {"form": form})


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated
    return render(request, "account/dashboard.html")


def index_view(request):
    # Optional home view
    return render(request, "account/index.html")

def platerecords_view(request):
    return render(request, "account/platerecords.html")

def super_view(request):
    return render(request, "account/super.html")

def logout_view(request):
    return render(request, "account/logout.html")

def userpage_view(request):
    uploaded_files = UploadedFile.objects.all()  # Get all uploaded files
    return render(request, "account/userpage.html", {'uploaded_files': uploaded_files})

def plate_view(request):
    return render(request, 'accounts/plateaction.html')


def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active

        # Loop through the rows and save them to the database
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming the first row is headers
            PlateRecord.objects.create(
                dv_number=row[0],
                serial_number=row[1],
                in_house_serial_number=row[2],
                status=row[3],
                date=row[4],
                remarks=row[5]
            )

        return render(request, 'admin_page.html', {'message': 'File uploaded successfully!'})

    form = ExcelUploadForm()
    return render(request, 'admin_page.html', {'form': form})

def import_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        UploadedFile.objects.create(file=uploaded_file)  # Save the uploaded file

        # Process the file based on its type
        if uploaded_file.name.endswith('.xml'):
            process_xml(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
            process_excel(uploaded_file)

        return redirect('userpage')  # Redirect to the user page after import

    return HttpResponse("Invalid request", status=400)

def process_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # Add your XML processing logic here...

def process_excel(excel_file):
    df = pd.read_excel(excel_file)
    # Add your Excel processing logic here...

def delete_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    uploaded_file.delete()  # Delete the file
    return redirect('userpage')  # Redirect back to the user page
