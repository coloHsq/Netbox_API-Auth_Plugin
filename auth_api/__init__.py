from extras.plugins import PluginConfig


class AuthApiConfigh(PluginConfig):
    # Plugin package name
    name = 'auth_api'

    # Human-friendly name and description
    verbose_name = 'Auth api'
    description = 'Api endpoint for users authentication that releases a token'

    # Plugin version
    version = '1.0'

    # Plugin author
    author = 'Davide Colombo'

    # Configuration parameters that MUST be defined by the user (if any)
    required_settings = []

    # Default configuration parameter values, if not set by the user
    default_settings = {
        'cache_timeout': 30  # seconds within which the AES key will be deleted
    }

    # Base URL path. If not set, the plugin name will be used.
    base_url = 'auth'


config = AuthApiConfigh
