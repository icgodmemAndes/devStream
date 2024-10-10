# Importación de dependencias

import traceback

from ..commands.base_command import BaseCommannd
from ..errors.errors import ApiError
from ..models.model import db, Blacklist


# Clase que contiene la logica de borrar tabla routes
class ResetRoutes(BaseCommannd):
    # Función que realiza eliminacion de blacklist
    def execute(self):
        try:
            db.session.query(Blacklist).delete()
            db.session.commit()
        except Exception as e:
            traceback.print_exc()
            raise ApiError(e)