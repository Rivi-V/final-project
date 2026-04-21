from urllib.parse import urlparse

from django.core.exceptions import ValidationError

REPOSITORY_HOST = 'github.com'
REPOSITORY_SERVICE_NAME = 'GitHub'


def validate_repository_url(url):
    normalized_url = (url or '').strip()
    if not normalized_url:
        return ''

    host = urlparse(normalized_url).netloc.lower()
    if host.startswith('www.'):
        host = host[4:]
    if host != REPOSITORY_HOST:
        raise ValidationError(f'Ссылка должна вести на {REPOSITORY_SERVICE_NAME}')
    return normalized_url
