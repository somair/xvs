import re

from django.core.exceptions import ValidationError

def validate_numerals(value):
    if not re.match('^[\d ]+$', value):
        raise ValidationError(u"You can only enter numbers and spaces here.")
