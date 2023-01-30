"""
Testing module
"""
from project.models import Data
from project.db import db


def test_status_code(client):
    """
    Response code should be 200
    """
    response = client.get("/")
    assert response.status_code == 200


def test_post_new_pdf(client, app):
    """
    PDF data count should equal to 1
    """
    data = {}
    data["file"] = open("file.pdf", "rb")
    response = client.post("/documents", data=data) 
    return_response = response.data.decode()
    assert return_response == "1"  # Assert response return with the PDF id
    assert response.status_code == 200

    with app.app_context():
        assert Data.query.count() == 1
        assert Data.query.first().id == 1
        db.session.query(Data).delete()  # Clear db after asserts
        db.session.commit()


def test_get_pdf_info_by_id(client, app):
    """
    PDF info should be returned
    """
    # Insert new PDF
    data = {}
    data["file"] = open("file.pdf", "rb")
    response = client.post("/documents", data=data)
    return_response = response.data.decode()
    assert return_response == "1"  # Assert response return with the PDF id
    assert response.status_code == 200

    response = client.get("/documents/1")
    assert response.status_code == 200

    with app.app_context():
        db.session.query(Data).delete()  # Clear db after asserts
        db.session.commit()


def test_get_pdf_text(client, app):
    """
    PDF text should be returned
    """
    data = {}
    data["file"] = open("file.pdf", "rb")
    response = client.post("/documents", data=data)
    return_response = response.data.decode()
    assert return_response == "1"  # Assert response return with the PDF id
    assert response.status_code == 200

    response = client.get("/text/1")
    return_response = response.data.decode()

    with app.app_context():
        assert return_response == Data.query.first().text
        db.session.query(Data).delete()  # Clear db after asserts
        db.session.commit()
