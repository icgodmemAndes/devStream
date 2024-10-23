import os

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import traceback
import uuid

from src.commands.base_command import BaseCommannd
from src.errors.errors import MissingToken, EmailBlacklisted, InvalidToken, ApiError
from src.models.base import db
from src.models.mail import MailBlocked
from src.validators.validators import CreateBlacklistSchema, validate_schema

AUTH_TOKEN = os.environ.get('API_SECRET', 'api_secret')

class CreateBlacklist(BaseCommannd):
    def __init__(self, data, ipaddress, headers):
        self.validateHeaders(headers)
        self.validateToken()
        self.validateRequest(data)
        self.id = uuid.uuid4()
        self.email = data['email']
        self.appUuid = data['appUuid']
        self.blockedReason = data['blockedReason']
        self.ipAddress = ipaddress
        self.createdAt = datetime.now()
        self.validateEmailAndUuid(self.email, self.appUuid)


    def validateRequest(self, data):
        validate_schema(data, CreateBlacklistSchema)
        # Validacion del request


    # Función que valida los headers
    def validateHeaders(self, headers):
        if not "Authorization" in headers:
            raise MissingToken
        self.token = headers["Authorization"]

    # Función que valida el token

    def validateToken(self):
        if AUTH_TOKEN != self.token.replace("Bearer ", ""):
            raise InvalidToken

    # Función que valida si existe un usuario con el username
    def validateEmailAndUuid(self, email, uuid_validate):
        userConsult = db.session.query(MailBlocked).filter_by(email=email,app_uuid=uuid_validate ).one_or_none()
        print(userConsult)
        if userConsult != None:
            raise EmailBlacklisted
    def execute(self):
        try:
            new_blacklist = MailBlocked(
                id=self.id,
                email=self.email,
                app_uuid=self.appUuid,
                blocked_reason=self.blockedReason,
                ip_address=self.ipAddress,
                created_at=self.createdAt
            )
            db.session.add(new_blacklist)
            db.session.commit()
            return {'id': self.id,
                    'msg': 'Blacklist agregada satisfactoriamente',
                    'createdAt': self.createdAt.replace(microsecond=0).isoformat()}
        except SQLAlchemyError as e: # pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
