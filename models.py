from flask_sqlalchemy import SQLAlchemy

from config import DISEASE_API_FIELDS

db = SQLAlchemy()


class Disease(db.Model):
    __tablename__ = "disease"

    id: int = db.Column(db.Integer, primary_key=True)
    country: str = db.Column(db.String(100), nullable=False)
    region: str = db.Column(db.String(100), nullable=False)
    population: int = db.Column(db.BigInteger, nullable=False)
    cases: int = db.Column(db.BigInteger, nullable=False)
    deaths: int = db.Column(db.BigInteger, nullable=False)
    recovered: int = db.Column(db.BigInteger, nullable=False)

    def to_dict(self, fields=DISEASE_API_FIELDS):
        return {
            field: getattr(self, field)
            for field in fields
        }
