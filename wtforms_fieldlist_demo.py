# -*- coding: utf-8 -*-
__author__ = 'florije'

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from flask.ext.babel import gettext
from wtforms import SelectField, TextField, FormField, FieldList, SubmitField
from flask.ext.wtf.html5 import TelField
from wtforms.validators import Optional, Required

app = Flask(__name__)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50))
    phone = db.relationship(lambda: PhoneNumber)


class PhoneNumber(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    phonetype = db.Column(db.String(10))
    number = db.Column(db.String(20))
    ext = db.Column(db.String(10))


class PhoneNumberForm(Form):
    phonetype = SelectField(gettext("Type"), choices=[(c, c) for c in ['Mobile', 'Home', 'Work', 'Fax', 'Other']])
    number = TelField(gettext("Number"), validators=[Required()])
    ext = TextField(gettext("Notes"), validators=[Optional()])

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(PhoneNumberForm, self).__init__(csrf_enabled=False, *args, **kwargs)


class ModelFieldList(FieldList):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        super(ModelFieldList, self).__init__(*args, **kwargs)
        if not self.model:
            raise ValueError("ModelFieldList requires model to be set")

    def populate_obj(self, obj, name):
        while len(getattr(obj, name)) < len(self.entries):
            newModel = self.model()
            db.session.add(newModel)
            getattr(obj, name).append(newModel)
        while len(getattr(obj, name)) > len(self.entries):
            db.session.delete(getattr(obj, name).pop())
        super(ModelFieldList, self).populate_obj(obj, name)


class UserForm(Form):
    username = TextField(gettext("Username"), validators=[Required()])
    phone = ModelFieldList(FormField(PhoneNumberForm), model=PhoneNumber)
    submit = SubmitField(gettext("Submit"))


@app.route("/")
def index():
    user = User.query.first()
    form = UserForm(obj=user)
    form.phone.min_entries = 3
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
    return render_template("page.html", form=form)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.add(User(username="Frank"))
    db.session.commit()
    app.run(debug=True)
