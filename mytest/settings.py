import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасное получение SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production-' + str(hash('buxoro-maktab')))

# DEBUG из переменных окружения
# Default True for development, use environment variable DEBUG=False for production
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = [
    '176.96.241.174', 
    'buxorobilimdonlarmaktabi.uz',
    'www.buxorobilimdonlarmaktabi.uz',
    'localhost',
    '127.0.0.1'
]

# Приложения
INSTALLED_APPS = [
    'jazzmin',  # Admin panel uchun zamonaviy dizayn
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'accounts',
    'tests_app',
    'analytics',  # Analytics va statistika
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
]

# 1) MIDDLEWARE: gzip middleware va cors yuqorisi moslashuvi
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',                    # <-- qo'shildi: response siqish
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',  # Cache middleware (yuqorida)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mytest.middleware.NoCacheMiddleware',
    'analytics.middleware.AnalyticsMiddleware',  # Analytics tracking
    'django.middleware.cache.FetchFromCacheMiddleware',  # Cache middleware (pastda)
]

ROOT_URLCONF = 'mytest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mytest.wsgi.application'

#PostgreSQL

DATABASES = { 
     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
     }
}
# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Интернационализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки безопасности для production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# CORS настройки
CORS_ALLOWED_ORIGINS = [
    "https://buxorobilimdonlarmaktabi.uz",
    "https://www.buxorobilimdonlarmaktabi.uz",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Кастомная модель пользователя
AUTH_USER_MODEL = 'accounts.User'

# Caching konfiguratsiyasi - performance uchun
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,
        }
    }
}

# Cache timeout'lar (sekundlarda)
CACHE_MIDDLEWARE_SECONDS = 60  # 1 daqiqa
CACHE_MIDDLEWARE_KEY_PREFIX = 'buxoro_maktab'

# Test vaqt limiti (daqiqada) - Word/TXT orqali yaratilgan testlar uchun
# Serverni sozlamalaridan olinadi, muhit o'zgaruvchisi orqali o'zgartirish mumkin
DEFAULT_TEST_TIME_LIMIT = int(os.environ.get('DEFAULT_TEST_TIME_LIMIT', 45))

# Fayl yuklash limitlari (1GB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 1024  # 1GB
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 1024  # 1GB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# WhiteNoise для статических файлов (уже настроен выше)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Jazzmin Settings
JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "Buxoro Bilimdonlar Maktabi Admin",

    # Title on the brand, and the login screen
    "site_header": "🎓 Buxoro Bilimdonlar Maktabi",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "books.ico",
    
    # Logo on login page
    "login_logo": None,
    
    # Logo for your site on dark backgrounds
    "site_logo_classes": "img-circle",

    # Welcome text on the login screen
    "welcome_sign": "Buxoro Bilimdonlar Maktabi Admin Paneliga Xush Kelibsiz 🎓",

    # Copyright on the footer
    "copyright": "© 2025 Buxoro Bilimdonlar Maktabi",

    # Field name on user model that contains avatar image
    "user_avatar": None,
    
    ############
    # Search bar #
    ############
    
    # Search bar in the top navbar
    "search_model": ["auth.User", "tests_app.Test"],

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Bosh Sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Saytga O'tish", "url": "/", "new_window": True},
        
        # Export credentials links
        {"name": "📥 O'qituvchilar Login", "url": "/admin/export-teachers-credentials/", "permissions": ["auth.view_user"]},
        {"name": "📥 O'quvchilar Login", "url": "/admin/export-students-credentials/", "permissions": ["auth.view_user"]},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "tests_app"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right
    "usermenu_links": [
        {"name": "Saytga O'tish", "url": "/", "new_window": True},
        {"name": "📥 O'qituvchilar Login", "url": "/admin/export-teachers-credentials/", "permissions": ["auth.view_user"]},
        {"name": "📥 O'quvchilar Login", "url": "/admin/export-students-credentials/", "permissions": ["auth.view_user"]},
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu
    "hide_apps": [],

    # Hide these models when generating side menu
    "hide_models": [],

    # List of apps to base side menu ordering off of
    "order_with_respect_to": ["accounts", "tests_app"],
    
    # Custom links for side menu
    "custom_links": {
        "accounts": [{
            "name": "📥 O'qituvchilar Login Export",
            "url": "/admin/export-teachers-credentials/",
            "icon": "fas fa-download",
            "permissions": ["auth.view_user"]
        }, {
            "name": "📥 O'quvchilar Login Export",
            "url": "/admin/export-students-credentials/",
            "icon": "fas fa-download",
            "permissions": ["auth.view_user"]
        }]
    },

    # Custom icons for side menu apps (Font Awesome icons)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.User": "fas fa-user-graduate",
        "accounts": "fas fa-user-shield",
        "tests_app": "fas fa-clipboard-list",
        "tests_app.Test": "fas fa-tasks",
        "tests_app.Question": "fas fa-question-circle",
        "tests_app.Answer": "fas fa-check-circle",
        "tests_app.Choice": "fas fa-list-ul",
        "tests_app.TestAttempt": "fas fa-clock",
        "tests_app.TestResult": "fas fa-chart-line",
        "tests_app.TestRetakeRequest": "fas fa-redo",
    },

    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    "custom_css": "css/admin_custom.css",
    "custom_js": None,
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
}

# Jazzmin UI Configuration - Zamonaviy dizayn
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",  # Yashil rang (maktab rangi)
    "accent": "accent-success",  # Yashil accent
    "navbar": "navbar-white navbar-light",  # Oq navbar
    "no_navbar_border": False,
    "navbar_fixed": True,  # Navbar doim yuqorida
    "layout_boxed": False,  # To'liq kenglik
    "footer_fixed": False,
    "sidebar_fixed": True,  # Sidebar doim chap tomonda
    "sidebar": "sidebar-dark-success",  # Yashil qora sidebar
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,  # Indent qilish
    "sidebar_nav_compact_style": True,  # Compact style
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",  # Zamonaviy flatly theme
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
}
