#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session,redirect
from application.base import BaseManager, render_jinja
from application.db import models
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
#login_manager = LoginManager()
render = render_jinja('static/templates/grade', encoding='utf-8',)

class GradeList(BaseManager):
    def get(self):
        return render.grade_lists()
    def post(self):
        pass
class GradeInput(BaseManager):
    def get(self):
        return render.grade_input()
    def post(self):
        params = request.form

        values = {
            'college':params.get('college'),
            'subject':params.get('subject'),
            'student_class':params.get('student_class'),
            'student_name':params.get('student_name'),
            'studnet_number':params.get('studnet_number'),
            'current_date':params.get('current_date')

        }
        return success2json("ff")

app = Blueprint('grade_app', __name__, template_folder='templates')
app.add_url_rule('/input', view_func=GradeInput.as_view('grade_input'))
app.add_url_rule('/lists', view_func=GradeList.as_view('grade_lists'))