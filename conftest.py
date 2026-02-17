import pytest
from zohidpy.app import ZohidPy

@pytest.fixture
def app():
    return ZohidPy()

@pytest.fixture
def test_client(app):
    return app.test_session()