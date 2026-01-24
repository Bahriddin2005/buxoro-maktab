from django.utils import timezone  # pyright: ignore[reportMissingImports]
from .models import UserActivity, PageView
import time


class AnalyticsMiddleware:
    """User activity va page views ni track qilish"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Request boshlanish vaqtini saqlash
        request._analytics_start_time = time.time()
        
        response = self.get_response(request)
        
        # Process response
        return self.process_response(request, response)
    
    def process_response(self, request, response):
        try:
            # Static files, admin panel va API endpointlarini skip qilish
            path = request.path
            
            # Skip qilish kerak bo'lgan pathlar
            skip_paths = [
                '/static/',
                '/media/',
                '/admin/static/',
                '/admin/jsi18n/',
                '/favicon.ico',
                '/__debug__/',
                '/api/',
            ]
            
            # Agar path skip qilish kerak bo'lsa, analytics'ni o'tkazib yuborish
            if any(path.startswith(skip) for skip in skip_paths):
                return response
            
            # Faqat 200 OK response'larni track qilish
            if response.status_code != 200:
                return response
            
            # IP address olish
            ip_address = self.get_client_ip(request)
            
            # User agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            
            # Page view ni saqlash (faqat muhim pathlar uchun)
            if hasattr(request, '_analytics_start_time'):
                response_time = (time.time() - request._analytics_start_time) * 1000  # milliseconds
                
                # Faqat response_time 1000ms dan kichik bo'lsa yoki authenticated user bo'lsa
                # Bu juda sekin request'larni filter qiladi
                if response_time < 1000 or request.user.is_authenticated:
                    PageView.objects.create(
                        path=path[:255],  # Max length limit
                        user=request.user if request.user.is_authenticated else None,
                        ip_address=ip_address,
                        response_time=response_time
                    )
        
        except Exception:
            # Xatolik analytics'ga ta'sir qilmasligi kerak
            pass
        
        return response
    
    def get_client_ip(self, request):
        """Real IP address ni olish"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def log_activity(user, activity_type, request=None, **kwargs):
        """
        User activity ni log qilish
        
        Usage:
            AnalyticsMiddleware.log_activity(user, 'login', request)
            AnalyticsMiddleware.log_activity(user, 'test_start', request, test_id=test.id)
        """
        try:
            ip_address = None
            user_agent = ''
            
            if request:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip_address = x_forwarded_for.split(',')[0]
                else:
                    ip_address = request.META.get('REMOTE_ADDR')
                
                user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            
            UserActivity.objects.create(
                user=user,
                activity_type=activity_type,
                ip_address=ip_address,
                user_agent=user_agent,
                test_id=kwargs.get('test_id'),
                session_duration=kwargs.get('session_duration')
            )
        
        except Exception:
            pass

