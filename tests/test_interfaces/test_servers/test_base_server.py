import pytest
import asyncio

from cbi_webengines.interfaces.servers import Server


def test_empty_server():
    with pytest.raises(NotImplementedError):
        asyncio.run(Server.async_serve())
