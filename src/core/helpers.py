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


def pluralization(number, string_of_words):
    """
    Returns the correct Russian form of noun depending of numeral
    :param number:
    :param string_of_words: string with three forms separated by space
    :return: string with noun in correct form
    """
    list_of_words = string_of_words.split()
    a = number % 10
    b = number % 100
    if a == 1 and b != 11:
        return list_of_words[0]
    elif a >= 2 and a <= 4 and (b < 10 or b >= 20):
        return list_of_words[1]
    else:
        return list_of_words[2]
