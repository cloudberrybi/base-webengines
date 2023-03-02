from cbi_webengines.interfaces import (
    Application,
    EngineRepository,
    servers,
)


class ApplicationRepository:
    @classmethod
    def create_application(
        cls,
        url_prefix: str = '/',
        engine: EngineRepository = EngineRepository(),
        server: servers.Server = servers.UvicornServer,
    ) -> Application:
        application = Application(engine, server, url_prefix)

        return application
