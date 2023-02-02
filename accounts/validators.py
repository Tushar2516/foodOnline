import os
from django.core.exceptions import ValidationError

#  Function for check the file extension
def allow_only_image_validator(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['.png','.jpg','.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only Allow File Extension: ' +str(valid_extensions))
    