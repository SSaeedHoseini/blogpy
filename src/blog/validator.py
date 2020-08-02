import os
from django.core.exceptions import ValidationError

valid_extentions = ['.png', '.jpg', ]


def validate_file_extention(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in valid_extentions:
        raise ValidationError('the extentions not supported.')
