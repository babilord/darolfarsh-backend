from datetime import timedelta
from django.conf import settings
from django.test.signals import setting_changed
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, 'REST_KNOX', None)

DEFAULTS = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'TOKEN_TTL': None,
    'NO_REMEMBER_ME': timedelta(hours=6),
    'USER_SERIALIZER': 'knox.serializers.UserSerializer',
    'CORS_ORIGIN_WHITELIST' : [
        'https://example.com',
        'https://sub.example.com',
        'http://localhost:8080',
        'http://localhost:3000',
        'http://localhost:3001',
        'http://127.0.0.1:9000',
        'https://daralfarsha.com',
        'http://daralfarsha.com'
    ]
}

IMPORT_STRINGS = {
    'SECURE_HASH_ALGORITHM',
    'USER_SERIALIZER',
}

knox_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    global knox_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'REST_KNOX':
        knox_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)


class CONSTANTS:
    '''
    Constants cannot be changed at runtime
    '''
    TOKEN_KEY_LENGTH = 8
    DIGEST_LENGTH = 128
    SALT_LENGTH = 16

    def __setattr__(self, *args, **kwargs):
        raise RuntimeException('''
            Constant values must NEVER be changed at runtime, as they are
            integral to the structure of database tables
            ''')
CONSTANTS = CONSTANTS()
