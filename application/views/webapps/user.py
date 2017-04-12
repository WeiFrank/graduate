#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session,redirect
from application.base import BaseManager, render_jinja
from application.db import models
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
#login_manager = LoginManager()
render = render_jinja('static/templates/user', encoding='utf-8',)

class UserCreate(BaseManager):

    def get(self):
        return render.user_create()

    def post(self):

        params = request.form
        identity = params.get('identity')
        print "((((((((((((", identity
        if identity == 's':
            check_exist = models.User.query.filter_by(id=params.get('student_number')).first()
            if check_exist:
                print check_exist.id
                return  exception2json('用户已经存在')
            values = {
                'id': params.get('student_number'),
                'name': params.get('student_name'),
                'password': params.get('student_password'),
                'mail': params.get('student_mail'),
                'college': params.get('student_college'),
                'subject': params.get('student_subject'),
                'class_': params.get('student_class'),
                'semester': params.get('student_time'),
                'role_id': params.get('student_role')
            }
            print "sssssssssssss", values
            models.User(values).save()
            return  success2json("用户注册成功")
        else:
            check_exist = models.User.query.filter_by(id=params.get('teacher_number')).first()
            if check_exist:
                return exception2json("用户已经存在")
            values = {
                "id":params.get('teacher_number'),
                "password":params.get('teacher_password'),
                "mail":params.get('teacher_mail'),
                "name": params.get('teacher_name'),
                "college": params.get('teacher_college'),
                "subject": params.get('teacher_subject'),
                "role_id": params.get('teacher_role'),
            }
            print "tttttttttt", values
            models.User(values).save()
            return success2json("用户注册成功")


class UserDelete(BaseManager):
    def POST(self):
        pass


class Login:
    def GET(self):
        pass
    def post(self, parmes):
        username = parmes.get('username', '')
        password = parmes.get('password', '')
        identity = parmes.get('identity', '')
        if identity == 'student':
            print "----------", identity
            check_user = models.User.query.filter_by(id=username).first()
            check_password = models.User.query.filter_by(password=password).first()
            if check_user:
                if check_password:
                    return redirect('/home')
            else:
                return exception2json("user not exist")
        elif identity == 'teacher':
            check_user = models.User.query.filter_by(id=username).first()
            check_password = models.User.query.filter_by(password=password).first()
            if check_user:
                if check_password:
                    return redirect('/home')
            else:
                return exception2json("user is not exist")
        else:
            return  render.user_login(tip="erong")





app = Blueprint('usercreate', __name__, template_folder='templates')
app.add_url_rule('/create', view_func=UserCreate.as_view('user_create'))
# app.add_url_rule('/teacher/create', view_func=UserTeacherCreate.as_view('teacher_create'))