from app import db
from flask_login import UserMixin
from app import login
@login.user_loader
def load_user(id):
    return User.query.get(id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique = True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(128))
    classType = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)  
