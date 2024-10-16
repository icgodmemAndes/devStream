import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_request_validator import RequestError, InvalidRequestError

from models.base import db
from errors.errors import ApiError
from blueprints.mail_bp import mail_blueprint

# PostgresSQL configuration
host = os.environ.get('RDS_HOSTNAME', 'localhost')
port = os.environ.get('RDS_PORT', 5432)
user = os.environ.get('RDS_USERNAME', 'postgres')
password = os.environ.get('RDS_PASSWORD', 'postgres')
database_name = os.environ.get('RDS_DB_NAME', 'mails')


def create_app():
    _app = Flask(__name__)
    _app.config['PROPAGATE_EXCEPTIONS'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{database_name}'
    _app.config['SQLALCHEMY_POOL_SIZE'] = 10
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app_context = _app.app_context()
    app_context.push()

    CORS(_app, origins="*")

    _app.register_blueprint(mail_blueprint)

    return _app


application = create_app()
db.init_app(application)
db.create_all()


@application.errorhandler(ApiError)
def handle_api_error(error):
    return jsonify({'message': error.message}), error.code


@application.errorhandler(RequestError)
def handle_request_error(error):
    if isinstance(error, InvalidRequestError):
        return str(error.to_dict()), 400
    return str(error), 400


if __name__ == "__main__":
    application.run(debug=True)
