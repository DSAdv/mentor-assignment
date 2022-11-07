import uuid

from flask import Flask, Blueprint, jsonify, session, render_template, redirect, url_for

from forms import LinkForm
from settings import DB_URI
from models import db, UserLink

bp = Blueprint('links', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = LinkForm()

    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

    short_link = None
    redirect_count = 0

    if form.validate_on_submit():
        existing_link = UserLink.query.filter_by(
            user_id=session['user_id'],
            link=form.link.data,
        ).first()

        if existing_link:
            short_link_id = existing_link.short_link
            redirect_count = existing_link.redirect_count
        else:
            link = UserLink(link=form.link.data,
                            short_link=abs(hash(form.link.data + session['user_id'])),
                            user_id=session['user_id'])
            db.session.add(link)
            db.session.commit()
            short_link_id = link.short_link
            redirect_count = link.redirect_count

        short_link = url_for('links.redirect_on_short_link', short_link=short_link_id, _external=True)

    return render_template('index.html',
                           title='Shorten your link',
                           form=form,
                           short_link=short_link,
                           redirect_count=redirect_count)


@bp.route('/<short_link>')
def redirect_on_short_link(short_link):
    link = UserLink.query.filter_by(short_link=short_link).first()
    print(link)
    if link:
        link.redirect_count += 1
        db.session.commit()
        return redirect(link.link)
    else:
        return render_template('404.html'), 404


@bp.route('/healthcheck')
def healthcheck():
    return jsonify({'status': 'ok'})


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

    db.init_app(app)
    return app
