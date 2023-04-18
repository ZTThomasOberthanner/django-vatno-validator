from django.core.exceptions import ValidationError
from django.core.validators import _lazy_re_compile
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


@deconstructible
class VATNoValidator(object):
    message = _('Enter a valid VAT number.')
    code = 'invalid'

    # Format according to
    # http://ec.europa.eu/taxation_customs/vies/faq.html#item_11
    regexes = {
        'AT': _lazy_re_compile(r'^ATU\d{8}$'),  # Austria
        'BE': _lazy_re_compile(r'^BE0\d{9}$'),  # Belgium
        'BG': _lazy_re_compile(r'^BG\d{9,10}$'),  # Bulgaria
        'CY': _lazy_re_compile(r'^CY\d{8}\w$'),  # Cyprus
        'CZ': _lazy_re_compile(r'^CZ\d{8,10}$'),  # Czech Republic
        'DE': _lazy_re_compile(r'^DE\d{9}$'),  # Germany
        'DK': _lazy_re_compile(r'^DK\d{2} \d{2} \d{2} \d{2}$'),  # Denmark
        'EE': _lazy_re_compile(r'^EE\d{9}$'),  # Estonia
        'EL': _lazy_re_compile(r'^EL\d{9}$'),  # Greece
        'ES': _lazy_re_compile(r'^ES[\w\d]\d{7}[\w\d]$'),  # Spain
        'FI': _lazy_re_compile(r'^FI\d{8}$'),  # Finland
        'FR': _lazy_re_compile(r'^FR[\w\d]{2} \d{9}$'),  # France
        'GB': _lazy_re_compile(r'^GB((\d{3} \d{4} \d{2})|(\d{3} \d{4} \d{2} \d{3})|((GD|HA)\d{3}))$'),  # United Kingdom
        'HR': _lazy_re_compile(r'^HR\d{11}$'),  # Croatia
        'HU': _lazy_re_compile(r'^HU\d{8}$'),  # Hungary
        'IE': _lazy_re_compile(r'^IE((\d[\d\w\+\*]\d{5}\w)|(\d{7}WI))$'),  # Ireland
        'IT': _lazy_re_compile(r'^IT\d{11}$'),  # Italy
        'LT': _lazy_re_compile(r'^LT\d{9,12}$'),  # Lithuania
        'LU': _lazy_re_compile(r'^LU\d{8}$'),  # Luxembourg
        'LV': _lazy_re_compile(r'^LV\d{11}$'),  # Latvia
        'MT': _lazy_re_compile(r'^MT\d{8}$'),  # Malta
        'NL': _lazy_re_compile(r'^NL\d{9}B\d{2}$'),  # The Netherlands
        'PL': _lazy_re_compile(r'^PL\d{10}$'),  # Poland
        'PT': _lazy_re_compile(r'^PT\d{9}$'),  # Portugal
        'RO': _lazy_re_compile(r'^RO\d{2,10}$'),  # Romania
        'SE': _lazy_re_compile(r'^SE\d{12}$'),  # Sweden
        'SI': _lazy_re_compile(r'^SI\d{8}$'),  # Slovenia
        'SK': _lazy_re_compile(r'^SK\d{10}$'),  # Slovakia
    }

    allowed_countries = regexes.keys()

    def __init__(self, message=None, code=None, allowed_countries=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if allowed_countries is not None:
            self.allowed_countries = allowed_countries

    def __call__(self, value):
        value = force_str(value)

        # Can't be valid
        if len(value) < 2:
            raise ValidationError(self.message, code=self.code)

        # Check if country index exists
        if (value[:2] not in self.regexes) or (
                value[:2] not in self.allowed_countries):
            raise ValidationError(self.message, code=self.code)

        regex = self.regexes[value[:2]]

        if not regex.match(value):
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, VATNoValidator) and
            (self.message == other.message) and
            (self.code == other.code)
        )
