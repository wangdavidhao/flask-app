"""
Models module
"""
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict
from .db import db

class Data(db.Model):
    """
    Data model in the database
    For storing PDF information
    """
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    meta = db.Column(MutableDict.as_mutable(JSON))
