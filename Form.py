#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:46
# @File    : Form.py
"""
表单类
"""

from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import Required
from flask_wtf import FlaskForm


# 登录表单
class Login_Form(FlaskForm):
    user_phone = StringField('手机号', validators=[Required()])
    user_passwd = PasswordField('密码', validators=[Required()])
    submit = SubmitField('登陆')

# 注册表单
class Register_Form(FlaskForm):
    user_phone = StringField('name', validators=[Required()])
    user_passwd = PasswordField('pwd', validators=[Required()])
    submit = SubmitField('register')

class open_question(FlaskForm):
    ques_ctt = StringField('描述你的问题',validators=[Required()])
    submit = SubmitField('zhihu一下')

class logout_user(FlaskForm):
    pass


class form_ans_new(FlaskForm):
    body = TextAreaField('写下你的看法！',validators=[Required()])
    submit = SubmitField('提交回答')

class form_ques_new(FlaskForm):
    body = TextAreaField('写下你的问题！', validators=[Required()])
    submit = SubmitField('提交回答')