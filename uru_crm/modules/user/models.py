# -*- coding: utf-8 -*-
"""
    uru_crm.modules.user
    ~~~~~~~~~~~~~~~~~~

    User model definition(s)
"""

from uuid import uuid4

from sqlalchemy import Column
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from uru_crm.types import DenormalizedText
from uru_crm.extensions import db
from uru_crm.utils import get_current_time, GENDER_TYPE, STRING_LEN
from uru_crm.modules.base import Base
from .constants import USER, USER_ROLE, ADMIN, INACTIVE, USER_STATUS


box_groupings = db.Table(
    'box_groupings',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('box_id', db.Integer(), db.ForeignKey('box.id'))
)


class Farm(Base):
    farm = db.Column(db.String(STRING_LEN), nullable=False, unique=True)
    phone_num = Column(db.String(STRING_LEN), nullable=False, default='test')
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    address = Column(db.String(STRING_LEN), nullable=False, default='test')


class Available_Veggie(Base):
    veggie = db.Column(db.String(STRING_LEN), nullable=False)
    farm = db.Column(db.String(STRING_LEN), nullable=False)
    quantity = db.Column(db.String(STRING_LEN), nullable=False)


class Box(Base):
    group = Column(db.Integer, nullable=False)
    veggies = db.Column(db.String(STRING_LEN), nullable=False, unique=True)
    date = Column(db.DateTime, nullable=False)


class User(Base, UserMixin):
    first_name = Column(db.String(STRING_LEN), nullable=False)
    last_name = Column(db.String(STRING_LEN), nullable=False)
    phone_num = Column(db.String(STRING_LEN), nullable=False)
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    address = Column(db.String(STRING_LEN), nullable=False)
    registered_at = Column(db.DateTime, default=get_current_time)
    box_size = Column(db.String(STRING_LEN), nullable=False)
    duration = Column(db.String(STRING_LEN), nullable=False)
    delivery_instructs = Column(db.Text)
    bad_veggies = Column(db.Text)
    user_grouping = Column(db.Integer, nullable=False, default=1)

    user_grouping = db.relationship('Box', secondary=box_groupings,
                            backref=db.backref('users', lazy='dynamic'))

    _password = Column('password', db.String(STRING_LEN), nullable=False, default=uuid4().hex)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)
    # Hide password encryption by exposing password field only.
    password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def reset_password(self):
        self.activation_key = str(uuid4())
        db.session.add(self)
        db.session.commit()

    def change_password(self):
        self.password = self.password.data
        self.activation_key = None
        db.session.add(self)
        db.session.commit()

    # ================================================================
    # One-to-many relationship between users and roles.
    role_code = Column(db.SmallInteger, default=USER)

    @property
    def role(self):
        return USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == ADMIN

    # ================================================================
    # One-to-many relationship between users and user_statuses.
    status_code = Column(db.SmallInteger, default=INACTIVE)

    @property
    def status(self):
        return USER_STATUS[self.status_code]

    # ================================================================
    # Follow / Following
    # followers = Column(DenormalizedText)
    # following = Column(DenormalizedText)
    #
    # @property
    # def num_followers(self):
    #     if self.followers:
    #         return len(self.followers)
    #     return 0
    #
    # @property
    # def num_following(self):
    #     return len(self.following)
    #
    # def follow(self, user):
    #     user.followers.add(self.id)
    #     self.following.add(user.id)
    #     user.followers = list(user.followers)
    #     self.following = list(self.following)
    #     db.session.commit()
    #
    # def unfollow(self, user):
    #     if self.id in user.followers:
    #         user.followers.remove(self.id)
    #         user.followers = list(user.followers)
    #         db.session.add(user)
    #     if user.id in self.following:
    #         self.following.remove(user.id)
    #         self.following = list(self.following)
    #         db.session.add(self)
    #     db.session.commit()
    #
    # def get_following_query(self):
    #     return User.query.filter(User.id.in_(self.following or set()))
    #
    # def get_followers_query(self):
    #     return User.query.filter(User.id.in_(self.followers or set()))
    #
    # def is_following(self, follower):
    #     return follower.id in self.following and self.id in follower.followers

    # ================================================================
    # Class methods

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(
                User.email.ilike(keyword)
            ))
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)

    def check_name(self):
        return User.query.filter(db.and_(User.email != self.id)).count() == 0
