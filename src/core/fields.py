import phonenumbers
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PhoneValidator(RegexValidator):
    """ Phone number regex validator comprises the following tokens:
        ^(\s*)?(\+)? - optional whitespace or plus sign in the begining
        ([- _():=+]?\d[- _():=+]?) - numbers and optional separators between them
        {7,14} - range of number of digits in the string
        (\s*) - optional whitespace in the ending of the string
    """
    regex = r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){7,13}(\s*)?$'
    message = _(
        'Телефонный номер должен иметь международный формат'
    )


class PhoneField(models.CharField):
    default_validators = [PhoneValidator()]
    description = _('Номер телефона')

    def get_prep_value(self, value):

        number_parsed = None
        try:
            number_parsed = phonenumbers.parse(value, region='RU')
        except phonenumbers.NumberParseException:
            try:
                number_parsed = phonenumbers.parse(value, region=None)
            except phonenumbers.NumberParseException:
                pass

        if number_parsed:
            value = phonenumbers.format_number(
                number_parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )

        return value
