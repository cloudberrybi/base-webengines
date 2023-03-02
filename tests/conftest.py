import pytest

from cbi_ddd.repositories import SettingsRepository
from cbi_webengines.interfaces.settings import BaseEngineAppSettings


@pytest.fixture(autouse=True)
def set_settings():
    SettingsRepository.settings_model = BaseEngineAppSettings
