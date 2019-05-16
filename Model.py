#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:45
# @File    : Model.py
"""
数据模型
"""

from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required
from Start import login_manger
from Start import db


class Users(UserMixin, db.Model):
    __tablename__ = 'user'  # 对应mysql数据库表
    user_id = db.Column(db.String(64), primary_key=True)
    user_phone = db.Column(db.String(64), unique=True, index=True)
    user_passwd = db.Column(db.String(64), unique=True, index=True)
    user_name = db.Column(db.String(64),unique=True,index=True)

    def __init__(self, user_phone, user_passwd):
        self.user_phone = user_phone
        self.user_passwd = user_passwd

    def get_id(self):
        # return unicode(self.id)
        return 1

    def __repr__(self):
        return '<User %r>' % self.user_phone

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False