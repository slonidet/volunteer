from django.conf import settings


def get_absolute_url(url):
    """
    Make absolute uri from url
    :param url: url without schema
    :return: absolute uri
    """
    if settings.SECURE_SSL_HOST:
        uri = 'https://{0}'.format(settings.SECURE_SSL_HOST)
    else:
        uri = 'http://{0}'.format(settings.DEFAULT_HOST)

    return uri + url


def pluralization(number, args):
    """
    Returns the correct Russsian form of noun depending of numeral
    :param number:
    :param args: list of noun forms
    :return: list
    """
    a = number % 10
    b = number % 100
    if a == 1 and b != 11:
        return args[0]
    elif a >= 2 and a <= 4 and (b < 10 or b >= 20):
        return args[1]
    else:
        return args[2]
