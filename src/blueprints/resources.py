from flask import jsonify, request, Blueprint

from ..commands.create import CreateBlacklist
from ..commands.reset import ResetRoutes
from ..errors.errors import InvalidDataError
import re

blacklist_blueprint = Blueprint('blacklist', __name__)


# Recurso que expone la funcionalidad healthcheck
@blacklist_blueprint.route('/blacklist/ping', methods=['GET'])
def health():
    return "pong"

@blacklist_blueprint.route("/", methods=["GET"])
def healthcheck():
    return jsonify({'status': 'UP'})

# Recurso que expone la funcionalidad reset blacklist
@blacklist_blueprint.route('/blacklist/reset', methods=['POST'])
def reset():
    ResetRoutes().execute()
    return jsonify({'msg': 'Todos los datos fueron eliminados'})

# Recurso que expone la funcionalidad create blacklist
@blacklist_blueprint.route('/blacklist', methods=['POST'])
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
