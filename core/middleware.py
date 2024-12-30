from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class CustomLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language = request.session.get('django_language') or request.COOKIES.get('django_language')

        if not language:
            language = 'kk'

        translation.activate(language)
        request.LANGUAGE_CODE = language