from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


def validator_the_year(value):
    if not (settings.YEAR < value < timezone.now().year):
        raise ValidationError(
            ('%(value)s is not a correcrt year!'),
            params={'value': value},
        )
