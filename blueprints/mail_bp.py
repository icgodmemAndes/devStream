import os
from flask import jsonify, request, Blueprint
from flask_request_validator import validate_params, Param, PATH, ValidRequest, NotEmpty, IsEmail

from models.base import db
from models.mail import MailBlocked
from errors.errrors import ApiError

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
