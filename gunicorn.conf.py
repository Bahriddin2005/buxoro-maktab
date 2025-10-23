bind = '127.0.0.1:8001'
workers = 8  # CPU cores * 2 + 1 (4 cores = 8 workers)
worker_class = 'gthread'  # Thread-based workers for I/O intensive tasks
threads = 10  # 10 threads per worker = 80 concurrent connections
worker_connections = 1000  # Max connections per worker
max_requests = 1000  # Restart workers after 1000 requests
max_requests_jitter = 50  # Random jitter to prevent thundering herd
preload_app = True  # Preload application for better performance
user = 'baxadev'
pythonpath = '/home/baxadev/my_test'
chdir = '/home/baxadev/my_test'
module = 'mytest.wsgi:application'
timeout = 120  # Increased timeout for long-running tests
keepalive = 5  # Keep connections alive
max_requests_jitter = 50
