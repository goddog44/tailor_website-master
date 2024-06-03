from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core import serializers
import os
import shutil
from .models import Dress, Tailor, database, Measurement
# Register your models here.
admin.site.register(Dress)
admin.site.register(Measurement)
admin.site.register(Tailor)

@admin.register(database)
class VillainAdmin(admin.ModelAdmin):
    change_form_template = 'villain_change_form.html'  # Update the template path

def backup_action(modeladmin, request, queryset):
    # Perform backup for the selected objects
    backup_files = []
    for obj in queryset:
        backup_file = backup_data(obj.__class__)
        backup_files.append(backup_file)

    # Prepare a zip file containing all backup files
    zip_filename = os.path.join(settings.MEDIA_ROOT, 'backup.zip')
    shutil.make_archive(zip_filename[:-4], 'zip', settings.MEDIA_ROOT, 'backup')

    # Create an HTTP response with the zip file for download
    with open(zip_filename, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=backup.zip'

    # Delete all backup files and the zip file
    delete_backup_files()
    os.remove(zip_filename)

    return response


def restore_action(modeladmin, request, queryset):
    # Access the uploaded file
    uploaded_file = request.FILES.get('file')

    if uploaded_file:
        # Save the uploaded file to a temporary location
        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp', uploaded_file.name)
        with open(temp_file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Restore the data from the uploaded backup file
        restore_data(queryset.model, temp_file_path)

        # Delete the temporary file
        os.remove(temp_file_path)

        return HttpResponse('Restore successful')
    else:
        return HttpResponse('No file uploaded for restore')


def backup_data(model):
    # Create a backup directory
    backup_dir = os.path.join(settings.MEDIA_ROOT, 'backup')
    os.makedirs(backup_dir, exist_ok=True)

    # Serialize the model data
    queryset = model.objects.all()
    serialized_data = serializers.serialize("json", queryset)

    # Write serialized data to a backup file
    backup_file = os.path.join(backup_dir, f"{model.__name__}_backup.json")
    with open(backup_file, "w") as file:
        file.write(serialized_data)

    return backup_file


def restore_data(model, backup_file):
    # Read the serialized data from the backup file
    with open(backup_file, "r") as file:
        serialized_data = file.read()

    # Deserialize and create objects from the serialized data
    objects = serializers.deserialize("json", serialized_data)
    for obj in objects:
        obj.save()

    # Delete the backup file
    os.remove(backup_file)


def delete_backup_files():
    # Delete all backup files
    backup_dir = os.path.join(settings.MEDIA_ROOT, 'backup')
    shutil.rmtree(backup_dir, ignore_errors=True)


# Register the backup and restore actions for VillainAdmin
VillainAdmin.actions = [backup_action, restore_action]