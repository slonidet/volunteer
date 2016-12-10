import phonenumbers
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PhoneValidator(RegexValidator):
    """ Phone number regex validator comprises the following tokens:

    ((\+7)|(8))?            either +7 or 8, optional
    [\s-]*                  separator, any number of spaces or "-" signs, optional
    [\(\[]?(\d{3})[\)\]]?   area code,  3 digits, in braces or not (e.g. 800, (800) or [800])
    [\s-]*                  separator, any number of spaces or "-" signs, optional
    (\d{3})                 trunk is 3 digits (e.g. '555')
    [\s-]*                  separator, any number of spaces or "-" signs, optional
    (\d{2})                 trunk is 3 digits (e.g. '555')
    [\s-]*                  separator, any number of spaces or "-" signs, optional
    (\d{2})                 rest 2 digits
    [\s-]*                  separator, any number of spaces or "-" signs, optional
    (\d{2})                 rest 2 digits
    [\s-]*                  separator, any number of spaces, optional
    (\d*)                   extension is optional and can be any number of digits
    """
    regex = r'^(\+?\d+)?[\s-]*[\(\[]?(\d{3})[\)\]]?[\s-]*(\d{3})[\s-]' \
            r'*(\d{2})[\s-]*(\d{2})[\s]*(\d*)$'
    message = _(
        'Телефонный номер должен иметь формат: +7 (908) 555-55-55 '
        'или 8 495 555-55-55. В качестве разделителя допускаются минус '
        'или пробел.'
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
