import os
from django.core.exceptions import ValidationError

# Announcements File Type Validaten Function
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1] # get the file extension
    valid_extensions = ['.pdf']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed: .pdf')

# File Size Validation
def valdate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024: # 5MB limit
        raise ValidationError('Maximum file size allowed is 5MB')