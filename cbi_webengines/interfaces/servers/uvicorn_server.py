import uvicorn

from cbi_ddd.repositories import SettingsRepository
from cbi_webengines.interfaces.settings import (
    BaseEngineAppSettings,
    WebAppSettings,
)

from .server import Server


class UvicornServer(Server): # ignore_coverage
    @classmethod
    async def async_serve(cls, **params):
        config: BaseEngineAppSettings = SettingsRepository.get_config()

        web_config: WebAppSettings = config.web if hasattr(config, 'web') else WebAppSettings()

        app = params.get('app', None)
        host = params.get('host', web_config.host)
        port = params.get('port', web_config.port)
        log_level = params.get('log_level', web_config.log_level)

        if app:
            server_config = uvicorn.Config(
                app,
                host=host,
                port=port,
                log_level=log_level,
            )
            server = uvicorn.Server(server_config)
            await server.serve()
