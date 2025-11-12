from django.http import HttpResponseBadRequest
import logging

logger = logging.getLogger(__name__)

class HttpOnlyMiddleware:
    """Middleware to reject HTTPS connections in development."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if request is using HTTPS
        if request.is_secure() or request.META.get('HTTP_X_FORWARDED_PROTO') == 'https':
            logger.warning(f"HTTPS request rejected from {request.META.get('REMOTE_ADDR', 'unknown')}")
            return HttpResponseBadRequest("This development server only supports HTTP connections. Please use http:// instead of https://")
        
        response = self.get_response(request)
        return response