from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(512), nullable=False)
    short_link = db.Column(db.String(255), nullable=False)
    redirect_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.String(255), nullable=False)
