from extras.plugins import PluginConfig


class AuthApiConfigh(PluginConfig):
    name = 'auth_api'
    verbose_name = 'Auth api'
    description = 'Api endpoint for users authentication that releases a token'
    version = '1.0'
    author = 'Davide Colombo'
    required_settings = []
    default_settings = {'cache_timeout': 30}  # seconds within which the AES key will be deleted
    base_url = 'auth'


config = AuthApiConfigh
