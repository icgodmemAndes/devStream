class ApiError(Exception):
    code = 500
    message = 'error base'

class InvalidDataError(ApiError):
    code = 404
    message = "Párametros de entrada invalidos"

# Clase que contiene la estructura de error cuando no esta registra el username
class EmailBlacklisted(ApiError):
    code = 409
    message = "El email y la aplicación ya se encuentran registradas"

# Clase que contiene la estructura de un error de tipo Bad Request
class BadRequest(ApiError):
    code = 400
    message = "Párametros de entrada invalidos"

# Clase que contiene la estructura de error cuando no se envia el token
class MissingToken(ApiError):
    code = 403
    message = "El token no está en el encabezado de la solicitud"

# Clase que contiene la estructura de error cuando el token no es valido o esta vencido
class InvalidToken(ApiError):
    code = 401
    message = "El token no es válido o está vencido"
    def __init__(self, code, message):
        self.code = code or self.code
        self.message = message or self.message