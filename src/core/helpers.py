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
