# Importación de dependencias

import traceback

from src.commands.base_command import BaseCommannd
from src.errors.errors import ApiError
from src.models.base import db
from src.models.mail import MailBlocked


# Clase que contiene la logica de borrar tabla routes
class ResetRoutes(BaseCommannd):
    # Función que realiza eliminacion de blacklist
    def execute(self):
        try:
            db.session.query(MailBlocked).delete()
            db.session.commit()
        except Exception as e:
            traceback.print_exc()
            raise ApiError(e)