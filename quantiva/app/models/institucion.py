from datetime import datetime
from app import db

class Institucion(db.Model):
    __tablename__ = 'institucion'

    id = db.Column(db.BigInteger,primary_key=True)
    nameshort = db.Column(db.String(50),nullable=False)
    namelarge = db.Column(db.String(255),nullable=False)
    direction = db.Column(db.String(255),nullable=True)
    tipo = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),default=datetime.utcnow,onupdate=datetime.utcnow)