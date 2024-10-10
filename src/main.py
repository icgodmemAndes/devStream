import sys

from dotenv import load_dotenv
from pathlib import Path

from flask import Flask, jsonify
from flask_restful import Api

import os

from .blueprints.resources import blacklist_blueprint
from .errors.errors import ApiError
from .models.model import db

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
env_path = Path('.') / '.env.development'
load_dotenv(dotenv_path=env_path)

# Constantes
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
APP_PORT = int(os.getenv("APP_PORT", default=3002))

# Configuracion app
def create_flask_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.register_blueprint(blacklist_blueprint)
    app_context = app.app_context()
    app_context.push()
    return app


app = create_flask_app()
db.init_app(app)
db.create_all()
api = Api(app)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description,
    }
    return jsonify(response), err.code


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=APP_PORT)
