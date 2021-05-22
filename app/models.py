from datetime import datetime

from flask_login import UserMixin

from app.database import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % self.name


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(1000), default=None, nullable=True)
    url = db.Column(db.String(1000))
    type = db.Column(db.SMALLINT, default=0)
    click_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=None, nullable=True)
    user = db.relationship('User', backref=db.backref('links', lazy=True))

    def add_new_click(self):
        self.click_count += 1
        link_stat = LinkStatistic()
        link_stat.date = datetime.now()
        db.session.add(link_stat)
        self.linkstatistics.append(link_stat)
        db.session.commit()

    def __repr__(self):
        return '<Link %r>' % self.name


class LinkStatistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))
    link = db.relationship('Link', backref=db.backref('linkstatistics', lazy=True))

    def __repr__(self):
        return '<LinkDate %r>' % self.date
