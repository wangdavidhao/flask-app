"""
Routes module
"""
from flask import Blueprint, render_template, request
from PyPDF2 import PdfReader

from .db import db
from .models import Data

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def get_index():
    """Get index page for uploading PDF
    ---
    responses:
      200:
        description: Returns index page
    """
    return render_template("index.html"), 200


@main.route("/documents/<pdf_id>", methods=["GET"])
def get_pdf_info_by_id(pdf_id):
    """Get PDF info by providing its ID
    ---
    parameters:
      - name: id
        type: string
    responses:
      200:
        description: Returns information about PDF inclunding metadata, size and its text
    """

    if not pdf_id.isdigit():
        return "ID must be string digit"

    try:
        data = db.session.query(Data).filter(Data.id == pdf_id).first()
        meta = data.meta.items()  # Extract key and values of metadata json
        return render_template(
            "pdf_info.html",
            pdf_id=data.id,
            pdf_size=data.size,
            pdf_text=data.text,
            pdf_meta=meta,
        )

    except:
        return render_template(
            "error.html", error="Error while trying to fetch a PDF info with its ID"
        )


@main.route("/text/<pdf_id>", methods=["GET"])
def get_text_by_id(pdf_id):
    """Get PDF text by providing its ID
    ---
    parameters:
      - name: id
        type: string
    responses:
      200:
        description: Returns PDF text
    """

    if not pdf_id.isdigit():
        return "ID must be string digit"

    try:
        data = db.session.query(Data).filter(Data.id == pdf_id).first()
        return render_template("pdf_text.html", text=data.text), 200

    except:
        return render_template(
            "error.html", error="Error while trying to fetch a PDF text with its ID"
        )


@main.route("/documents", methods=["POST"])
def post_pdf():
    """Post a new PDF file
    ---
    parameters:
      - name: file
        in: path
        type: file
        required: true
        content_type: ['application/pdf']
    responses:
      200:
        description: Returns PDF string ID
    """
    pdf_file = request.files["file"]  # Get file data

    if not pdf_file:
        return "Missing file"

    extension = pdf_file.filename.split(".")[1]  # Get file'x extension

    if extension != "pdf":
        return "Not a PDF file"

    size = len(request.files["file"].read())  # Get file size

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    new_data = Data(size=size, text=text, meta=reader.metadata)  # Creation of new data
    db.session.add(new_data)
    db.session.commit()

    try:
        return_id = new_data.id
        return str(return_id)
    except:
        return "Error returning new PDF id"

