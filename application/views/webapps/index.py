#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import request, Blueprint,redirect, session
from application.db import models
from application.base import BaseManager, render_jinja

import json
render = render_jinja('static/templates', encoding='utf-8')

class Home(BaseManager):
    def __init__(self):
        pass
    def get(self):

        username = session.get('username',None)
        user = models.User.query.filter_by(id=username).first()
        print '-----------', user
        if user:
            return render.home(user=user)
        else:
             return redirect('/login')

class Login(BaseManager):
    def get(self):
        return render.user_login(tip='')

    def post(self):
        params = request.form
        username = params.get('username', '')
        password = params.get('password', '')
        identity = params.get('identity', '')
        print  username,  password,identity
        if identity == 'student':
            print "----------", identity
            check_user = models.User.query.filter_by(id=username).first()
            check_password = models.User.query.filter_by(password=password).first()
            if check_user:
                if check_password:
                    # dic = {check_user.student_number:check_user.student_number}
                    # session.update(dic)
                    session['username'] = check_user.id
                    # session['college'] = check_user.college
                    # session['subject'] = check_user.subject
                    # session['class_'] = check_user.class_
                    # session['role'] = check_user.role
                    return redirect('/home')
                else:
                    return render.user_login(tip=json.dumps("密码错误"))
            else:
                return render.user_login(tip=json.dumps("用户不存在"))
        elif identity == 'teacher':
            check_user = models.User.query.filter_by(id=username).first()
            check_password = models.User.query.filter_by(password=password).first()
            if check_user:
                if check_password:
                    session['username'] = check_user.id
                    # session['college'] = check_user.college
                    # session['subject'] = check_user.subject
                    return redirect('/home')
                else:
                    return render.user_login(tip=json.dumps("密码错误"))
            else:
                return render.user_login(tip=json.dumps("u'用户不存在'"))
        else:
            return render.user_login(tip=json.dumps("erong"))


app = Blueprint('login_home', __name__, template_folder='templates')
app.add_url_rule('/home', view_func=Home.as_view('home'))
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/', view_func=Login.as_view('login_another'))