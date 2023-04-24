from api_client.plugins.base import BasePlugin
from api_client.plugins.validator import ValidatorPlugin, ValidatorPluginSettings
from api_client.plugins.retry import RetryPlugin, RetryPluginSettings
from api_client.plugins.cache import CachePlugin, CachePluginSettings
from api_client.plugins.exceptions import NotFoundPluginForSettings


SettingsPluginMapper = {
    ValidatorPluginSettings: ValidatorPlugin,
    RetryPluginSettings: RetryPlugin,
    CachePluginSettings: CachePlugin,
}

AnyPluginSettings = (
    ValidatorPluginSettings
    | RetryPluginSettings
    | CachePluginSettings
)


__all__ = (
    "BasePlugin",
    "CachePlugin",
    "RetryPlugin",
    "ValidatorPlugin",
    "ValidatorPluginSettings",
    "RetryPluginSettings",
    "CachePluginSettings",
    "cache_key_builder",
    "SettingsPluginMapper",
    "NotFoundPluginForSettings",
    "AnyPluginSettings",
)
