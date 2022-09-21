from django.utils.deprecation import MiddlewareMixin

from web.decorators import Tracer


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.tracer = Tracer()

