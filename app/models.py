from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token
from flask_login import UserMixin

from app.database import db
from app.modules.link_hash import hash_generator


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))

    def get_token(self, expire_time=1):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id,
            expires_delta=expire_delta,
        )
        return token

    def __repr__(self):
        return '<User %r>' % self.name


class FullLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), unique=True)

    @classmethod
    def get_or_create(cls, url: str, **kwargs):
        link = cls.query.filter_by(url=url).first()
        if not link:
            link = FullLink()
            link.url = url
            db.session.add(link)
            db.session.commit()
        return link

    def __repr__(self):
        return '<Link %r>' % self.name


class ShortLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(30),
        unique=True,
        default=hash_generator(),
    )
    description = db.Column(db.String(1000), default=None, nullable=True)
    type = db.Column(db.SMALLINT, default=0)
    click_count = db.Column(db.Integer, default=0)
    full_link_id = db.Column(db.Integer, db.ForeignKey('full_link.id'), default=None, nullable=True)
    full_link = db.relationship('FullLink', backref=db.backref('short_links', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=None, nullable=True)
    user = db.relationship('User', backref=db.backref('links', lazy=True))
    statistics = db.relationship('LinkStatistic', cascade="all,delete", backref=db.backref('short_link'))

    @classmethod
    def get_or_create(cls, user, full_link: FullLink, link_type:int, **kwargs):
        """Вернуть или создать объект с заданными параметрами.

        :param user: Владелец ссылки.
        :param full_link: Полная ссылка.
        :param link_type: Тип доступа к ссылке.
        :param kwargs: Может содержать: name - кастомное имя ссылки, description - доп. описание.
        :return ShortLink: Объект ShortLink.
        """
        short_link = ShortLink.query.filter_by(
            user=user,
            full_link=full_link,
            type=link_type
        ).first()
        if not short_link:
            short_link = ShortLink()
            short_link.full_link = full_link
            short_link.user = user
            short_link.type = link_type
            short_link.description = kwargs.get('description')
            if kwargs.get('name'):
                short_link.name = kwargs.get('name')
            db.session.add(short_link)
            db.session.commit()
        return short_link

    def add_new_click(self):
        self.click_count += 1
        link_stat = LinkStatistic()
        link_stat.date = datetime.now()
        db.session.add(link_stat)
        self.statistics.append(link_stat)
        db.session.commit()


class LinkStatistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    short_link_id = db.Column(db.Integer, db.ForeignKey('short_link.id'))

    def __repr__(self):
        return '<LinkDate %r>' % self.date
