from flask import Flask, Blueprint, jsonify

from settings import DB_URI
from models import db

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
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

    db.init_app(app)

    return app
