from django.shortcuts import render
import csv
import os
import uuid
import random
import string
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

def upload_csv(request):
    if request.method == 'POST':
        # Handle the uploaded file
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        uploaded_file_path = fs.path(filename)

        # Process the CSV
        processed_data = []
        with open(uploaded_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Get the header
            processed_data.append(header + ['Generated Code'])  # Add new column for codes

            for row in csv_reader:
                generated_code = uuid.uuid4().hex[:16]  # Generate a 16-character hex code
                processed_data.append(row + [generated_code])

        # Save the processed data to a new CSV file
        processed_filename = f'processed_{csv_file.name}'
        processed_file_path = fs.path(processed_filename)
        with open(processed_file_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(processed_data)

        # Provide the download link
        processed_file_url = fs.url(processed_filename)

        # Remove the uploaded file after processing
        os.remove(uploaded_file_path)

        return render(request, '/account/super.html', {'processed_file': processed_file_url})

    return render(request, 'account/super.html')

# code_generator/views.py
