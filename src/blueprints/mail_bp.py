import os
from flask import jsonify, request, Blueprint
from flask_request_validator import validate_params, Param, PATH, ValidRequest, NotEmpty, IsEmail

from src.commands.create import CreateBlacklist
from src.commands.reset import ResetRoutes
from src.errors.errors import ApiError, InvalidDataError
from src.models.base import db
from src.models.mail import MailBlocked

mail_blueprint = Blueprint('emails', __name__, url_prefix='/')

api_secret = os.environ.get('API_SECRET', 'api_secret')


@mail_blueprint.route('/ping', methods=['GET'])
@mail_blueprint.route('/ping/', methods=['GET'])
def ping():
    return "pong", 200


@mail_blueprint.route('/blacklists/<string:email>', methods=['GET'])
@mail_blueprint.route('/blacklists/<string:email>/', methods=['GET'])
@validate_params(Param('email', PATH, str, rules=[NotEmpty(), IsEmail()]))
def get_mail_blocked(_valid: ValidRequest, email: str):
    validate_authorization(request.headers.get('Authorization'))
    mail_response = db.session.query(MailBlocked).filter_by(email=email).one_or_none()
    return jsonify({
        'is_blocked': False if mail_response is None else True,
        'blocked_reason': '' if mail_response is None else mail_response.blocked_reason,
    }), 200


def validate_authorization(authorization):
    if authorization != f'Bearer {api_secret}':
        raise ApiError(401, 'Not authorized')

@mail_blueprint.route("/", methods=["GET"])
def healthcheck():
    return jsonify({'status': 'UP', 'version': 2})

# Recurso que expone la funcionalidad reset blacklist
@mail_blueprint.route('/blacklists/reset', methods=['POST'])
def reset():
    ResetRoutes().execute()
    return jsonify({'msg': 'Todos los datos fueron eliminados'})

# Recurso que expone la funcionalidad create blacklist
@mail_blueprint.route('/blacklists', methods=['POST'])
def create_blacklist():
    try:
        requestData = request.get_json()
        headers = request.headers
        ipAddress = request.remote_addr
        result = CreateBlacklist(requestData, ipAddress, headers).execute()
        print(result)
        return jsonify(result), 201

    except InvalidDataError:
        return "", 404
