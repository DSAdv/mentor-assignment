from flask import Flask, Blueprint, jsonify


bp = Blueprint('links', __name__)


@bp.route('/')
def index():
    return 'Hello world'


@bp.route('/healthcheck')
def healthcheck():
    return jsonify({'status': 'ok'})


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    return app
