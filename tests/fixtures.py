import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'DEBUG': True,
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
