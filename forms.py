from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class LinkForm(FlaskForm):
    link = StringField('User Link', [validators.DataRequired(),
                                     validators.URL(),
                                     validators.Length(min=5, max=255)])
    submit = SubmitField('Submit')
