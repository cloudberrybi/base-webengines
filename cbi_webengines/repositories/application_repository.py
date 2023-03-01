from cbi_webengines.interfaces import (
    Application,
    engines,
    servers,
)


class ApplicationRepository:
    @classmethod
    def create_application(
        cls,
        url_prefix: str = '/',
        engine: engines.Engine = engines.FastAPIEngine,
        server: servers.Server = servers.UvicornServer,
    ) -> Application:
        application = Application(engine, server, url_prefix)

        return application
