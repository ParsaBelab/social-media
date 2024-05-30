from django.core.exceptions import ValidationError


def file_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('maximum file size is 1MB')
