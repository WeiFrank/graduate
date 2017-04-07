#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session,redirect
from application.base import BaseManager, render_jinja
from application.db import models
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
#login_manager = LoginManager()
render = render_jinja('static/templates/user', encoding='utf-8',)

class UserStudentCreate(BaseManager):

    def get(self):
        return render.student_create()

    def post(self):
        values = {}
        params = request.form
        check_exist = models.UserStudent.query.filter_by(student_number=params.get('student_number')).first()
        if check_exist:
            print check_exist.student_number
            return  exception2json('用户已经存在')
        values = {
            'student_number': params.get('student_number'),
            'password': params.get('password'),
            'e_mail':params.get('e_mail')
        }
        print "sssssssssssss", values
        user_student = models.UserStudent(values).save()
        return  success2json(user_student)
class UserTeacherCreate(BaseManager):
    def __init__(self):
        pass
    def get(self):
        return  render.teacher_create()
    def post(self):
        params = request.form
        check_exist = models.UserTeacher.query.filter_by(teacher_number=params.get('teacher_number')).first()
        if check_exist:
            return exception2json("用户已经存在")
        values = {
            "teacher_number":params.get('teacher_number'),
            "password":params.get('password'),
            "e_mail":params.get('e_mail')
        }
        print "tttttttttt", values
        user_teacher = models.UserTeacher(values).save()
        return success2json(user_teacher)


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
            print "----------",identity
            check_user = models.UserStudent.query.filter_by(student_number=username).first()
            check_password = models.UserStudent.query.filter_by(password=password).first()
            if check_user:
                if check_password:
                    return redirect('/home')
            else:
                return exception2json("user not exist")
        elif identity == 'teacher':
            check_user = models.UserTeacher.query.filter_by(teacher_number=username).first()
            check_password = models.UserTeacher.query.filter_by(password=password).first()
            if check_user:
                if check_password:
                    return redirect('/home')
            else:
                return exception2json("user is not exist")
        else:
            return  render.user_login(tip="erong")





app = Blueprint('usercreate', __name__, template_folder='templates')
app.add_url_rule('/student/create', view_func=UserStudentCreate.as_view('student_create'))
app.add_url_rule('/teacher/create', view_func=UserTeacherCreate.as_view('teacher_create'))