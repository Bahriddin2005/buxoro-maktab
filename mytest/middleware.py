"""
Custom middleware for preventing browser caching on test pages
"""

class NoCacheMiddleware:
    """
    Middleware to add no-cache headers to specific URLs
    This prevents browser from caching test pages and showing stale data
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Test sahifalari uchun cache'ni o'chirish
        if request.path.startswith('/tests/') and '/take/' in request.path:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response

