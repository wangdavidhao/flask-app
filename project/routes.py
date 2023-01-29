"""
Routes module
"""
from flask import request, Blueprint, render_template
from PyPDF2 import PdfReader
from .models import Data
from .db import db

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def get_index():
    """Get index page
    ---
    responses:
      200:
        description: Index page
    """
    return render_template("index.html")


@main.route("/documents/<int:pdf_id>", methods=["GET"])
def get_pdf_info_by_id(pdf_id):
    """Get PDF info by providing its ID
    ---
    parameters:
      - id: string
    responses:
      200:
        description: Information about PDF inclunding author, size and its text
    """

    data = db.session.query(Data).filter(Data.id == pdf_id).first()

    if not data:
        return render_template(
            "error.html", error="Error while trying to fetch a PDF info with its ID"
        )
    return render_template(
        "pdf_info.html",
        pdf_title=data.metadata,
        pdf_id=data.id,
        pdf_size=data.size,
        pdf_text=data.text,
        pdf_meta=data.meta,
    )


@main.route("/text/<int:pdf_id>", methods=["GET"])
def get_text_by_id(pdf_id):
    """Get PDF text by providing its ID
    ---
    parameters:
      - id: string
    responses:
      200:
        description: PDF text
    """

    data = db.session.query(Data).filter(Data.id == pdf_id).first()

    if not data:
        return render_template(
            "error.html", error="Error while trying to fetch a PDF text with its ID"
        )
    return data.text


@main.route("/documents", methods=["POST"])
def post_pdf():
    """Post a new PDF file
    ---
    responses:
      200:
        description: PDF ID number
    """
    pdf_file = request.files["file"]  # Get file data
    extension = pdf_file.filename.split(".")[1]  # Get file'x extension
    size = len(request.files["file"].read())  # Get file size

    if extension != "pdf":
        return "Not a PDF file"

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    new_data = Data(size=size, text=text[:10], meta=reader.metadata)
    db.session.add(new_data)
    db.session.commit()

    return str(new_data.id)
