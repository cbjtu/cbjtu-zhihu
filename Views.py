#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1 14:45
# @File    : Views.py
"""
视图模型
"""

from flask import render_template, Blueprint, redirect, url_for, flash, request
from Start import login_manger
from Form import Login_Form, Register_Form, open_question, form_ans_new, form_ques_new
from Model import Users
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required
from Start import db
import pymysql as pm
import random, datetime


blog = Blueprint('blog', __name__)  # 蓝图


@blog.route('/')
def index():
    form = Login_Form()
    return render_template('login.html', form=form)

"""
@blog.route('/index')
def l_index():
    form = Login_Form()
    return render_template('login.html', form=form)
"""

@blog.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    qq = open_question()
    if form.validate_on_submit():
        user = Users.query.filter_by(user_phone=form.user_phone.data).first()
        print(user)
        if user is not None and user.user_passwd == form.user_passwd.data:
            login_user(user)
            flash('登录成功')
            conn = pm.connect('localhost','xiaobing','9838','zhihu')
            cur = conn.cursor()
            sql = "SELECT ans.ans_ctt, ans.ans_time, ans.ans_like, ques.ques_ctt, " \
                  "user.user_name, ans.ans_quesid FROM (ans " \
                  "INNER JOIN ques on ques.ques_id = ans.ans_quesid) " \
                  "INNER JOIN user on user.user_id = ans.ans_ansid"
            cur.execute(sql)
            ques = cur.fetchall()
            conn.close()
            form.user_name = user.user_name
            fq = form_ques_new();
            return render_template('ok.html', user_phone=form.user_phone.data,
                                   user_name=form.user_name, ques=ques,qq=qq,fq=fq)
        else:
            flash('用户名或密码错误')
            return render_template('login.html',form=form)


@blog.route('/ok', methods=['GET', 'POST'])
def ok():
    conn = pm.connect('localhost', 'xiaobing', '9838', 'zhihu')
    cur = conn.cursor()
    sql = "SELECT * FROM ans"
    cur.execute(sql)
    ans = cur.fetchall()
    conn.close()
    return render_template('anslist.html', ans=ans)



# 用户登出
@blog.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登录')
    return redirect(url_for('login.html'))


@blog.route('/register', methods=['GET', 'POST'])
def register():
    form = Register_Form()
    if form.validate_on_submit():
        user = Users(user_phone=form.user_phone.data, user_passwd=form.user_passwd.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('login.html'))
    return render_template('register.html', form=form)

@blog.route('/ans/<ques_id>', methods=['GET','POST'])
def anslist(ques_id):
    print(ques_id)
    conn = pm.connect('localhost', 'xiaobing', '9838', 'zhihu')
    cur = conn.cursor()
    cur.execute("SELECT ans.ans_time, ans.ans_ctt, ans.ans_like, ans.ans_com, user.user_name, "
                "user.user_description FROM ans " \
          "INNER JOIN user ON user.user_id=ans.ans_ansid " \
          "WHERE ans.ans_quesid = %s",(ques_id,))
    ans = cur.fetchall()
    cur2 = conn.cursor()
    cur2.execute("SELECT ques.ques_ctt FROM ques WHERE ques.ques_id = %s",ques_id)
    ques = cur2.fetchall()
    print(ans)
    print(ques)
    conn.close()
    form=form_ans_new()
    return render_template('anslist.html', ans=ans, ques=ques, form=form, ques_id=ques_id)

@blog.route('/ans_new', methods=['GET', 'POST'])
def ans_new():
    form = form_ans_new()
    conn = pm.connect('localhost', 'xiaobing', '9838', 'zhihu')
    cur = conn.cursor()
    print("request here")
    print(request.form)
    print(request.args)
    sql = 'INSERT INTO ans(ans_id,ans_ansid,ans_time,ans_ctt,ans_quesid) VALUES(%s,%s,%s,%s,%s)'
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(sql,('a0'+str(random.randint(1,9))+str(random.randint(1,9)),
                     'u001',dt,form.body.data,'2'))
    conn.commit()
    conn.close()
    ff = Login_Form();
    return render_template('login.html', form=ff)

@blog.route('/ques_new', methods=['GET', 'POST'])
def ques_new():
    form = form_ques_new()
    conn = pm.connect('localhost', 'xiaobing', '9838', 'zhihu')
    cur = conn.cursor()
    print(request.args)
    sql = 'INSERT INTO ques(ques_id,ques_askerid,ques_time,ques_ctt) VALUES(%s,%s,%s,%s)'
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ques_id = str(random.randint(1,9))+str(random.randint(1,9))
    cur.execute(sql,(ques_id,
                     'u001',dt,form.body.data))
    sql = 'INSERT INTO ans(ans_id,ans_ansid,ans_time,ans_ctt,ans_quesid) VALUES(%s,%s,%s,%s,%s)'
    cur.execute(sql,('a0'+str(random.randint(1,9))+str(random.randint(1,9)),
                     'u001',dt,form.body.data,ques_id))
    conn.commit()
    conn.close()
    ff = Login_Form();
    return render_template('login.html', form=ff)
