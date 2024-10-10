import os

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import traceback
import uuid

from ..commands.base_command import BaseCommannd
from ..errors.errors import ApiError, MissingToken, InvalidToken, EmailBlacklisted
from ..models.model import db, Blacklist
from ..validators.validators import validate_schema, CreateBlacklistSchema

AUTH_TOKEN = os.environ["TOKEN"]

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
        userConsult = Blacklist.query.filter(Blacklist.email == email, Blacklist.app_uuid == uuid_validate).first()
        if userConsult != None:
            raise EmailBlacklisted
    def execute(self):
        try:
            new_blacklist = Blacklist(
                id=self.id,
                email=self.email,
                app_uuid=self.appUuid,
                blocked_reason=self.blockedReason,
                ip_address=self.ipAddress,
                createdAt=self.createdAt
            )
            db.session.add(new_blacklist)
            db.session.commit()
            return {'id': self.id,
                    'msg': 'Blacklist agregada satisfactoriamente',
                    'createdAt': self.createdAt.replace(microsecond=0).isoformat()}
            return {new_blacklist}
        except SQLAlchemyError as e: # pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
