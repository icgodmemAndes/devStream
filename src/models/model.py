from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

# Clase que cotiene la definición del modelo de base de datos de Routes
class Blacklist(db.Model):
    __tablename__ = "blacklist"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), nullable=False)
    app_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(256), nullable=True)
    createdAt = db.Column(DateTime, default=datetime.utcnow)

# Clase que autogenera el esquema del modelo Routes
class BlacklistSchema(SQLAlchemyAutoSchema):
    id = fields.String()

    class Meta:
        model = Blacklist
        load_instance = True