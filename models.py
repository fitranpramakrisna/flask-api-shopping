from config import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)


class Shopping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


db.create_all()
