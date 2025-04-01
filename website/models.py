from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #notes belong to one user
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    tag = db.Column(db.String(100))
    tag_color = db.Column(db.String(7))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') #one user can owns n notes

class SharedPermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    email = db.Column(db.String(150))
    can_edit = db.Column(db.Boolean, default=False)

    note = db.relationship('Note', backref='shared_permissions')
