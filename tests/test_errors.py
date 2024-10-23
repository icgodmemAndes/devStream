from src.errors.errors import ApiError, InvalidDataError, EmailBlacklisted, BadRequest, MissingToken, InvalidToken


class TestErrors():
    def test_api_error(self):
        result = ApiError()
        assert result.code == 500
        assert result.message == "error base"

    def test_invalid_data_error(self):
        result = InvalidDataError()
        assert result.code == 404
        assert result.message == "Párametros de entrada invalidos"

    def test_email_black_listed_error(self):
        result = EmailBlacklisted()
        assert result.code == 409
        assert result.message == "El email y la aplicación ya se encuentran registradas"

    def test_bad_request_error(self):
        result = BadRequest()
        assert result.code == 400
        assert result.message == "Párametros de entrada invalidos"

    def test_missing_token_error(self):
        result = MissingToken()
        assert result.code == 403
        assert result.message == "El token no está en el encabezado de la solicitud"

    def test_invalid_token_error(self):
        result = InvalidToken()
        assert result.code == 401
        assert result.message == "El token no es válido o está vencido"