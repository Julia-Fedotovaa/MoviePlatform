from rest_framework.exceptions import ValidationError

def validate_title(value):
    if len(value) < 2:
        raise ValidationError("Название должно содержать не менее 2 символов.")

    return value
