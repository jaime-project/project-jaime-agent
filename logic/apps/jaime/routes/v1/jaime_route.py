import yaml
from flask import Blueprint, jsonify, request
from logic.apps.jaime.services import jaime_service
import time

blue_print = Blueprint('jaime', __name__, url_prefix='/api/v1/jaime')


@blue_print.route('/', methods=['DELETE'])
def delete():

    jaime_service.disconnect_with_jaime()
    time.sleep(1)
    jaime_service.connect_with_jaime()

    return '', 200


@blue_print.route('/clusters/test', methods=['POST'])
def cluster_test():

    s = request.json
    return jsonify(jaime_service.test_cluster(s['url'], s['token'], s['type'])), 200