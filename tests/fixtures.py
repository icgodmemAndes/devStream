import datetime
from unittest.mock import patch
import pytest
from src.main import create_flask_app
from src.models.model import db

@pytest.fixture(autouse=True)
def app():
    application = create_flask_app()
    application.config.update({
        "TESTING": True
    })
    db.init_app(application)
    db.create_all()

    yield application
    db.session.rollback()
    db.session.close()
    db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def mock_datetime_now():
    class MockedDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2024, 12, 11, 20, 20, 53)

    with patch('datetime.datetime', MockedDatetime):
        yield
