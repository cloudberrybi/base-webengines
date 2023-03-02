from cbi_ddd.interfaces import BaseAppSettings

from .web_settings import WebAppSettings
from .cors_settings import CORSSettings


class BaseEngineAppSettings(BaseAppSettings):
    web: WebAppSettings = WebAppSettings()
    cors: CORSSettings = CORSSettings()
