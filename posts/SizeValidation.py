from django.core.exceptions import ValidationError


def file_size(value):  # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('حداکثر حجم مجاز 2 مگابایت میباشد')
