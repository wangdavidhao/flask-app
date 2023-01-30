import pytest

from project.app import create_app, db


@pytest.fixture()
def app():
    app = create_app("sqlite:////tmp/test-pdf-app") #We pass the test db URI

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()