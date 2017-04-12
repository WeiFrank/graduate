#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session,redirect
from application.base import BaseManager, render_jinja
from application.db import models
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
#login_manager = LoginManager()
render = render_jinja('static/templates/grade', encoding='utf-8',)

class GridGrade(BaseManager):
    def get(self):
        params = request.args
        # print "##############",params.get('page')
        filters = {}
        panger = Pager()
        page, total_paper, records, rows = panger.grid_rows_query(params=params, table='grade', mode='count')
        modelObject = models.GradeUser.query
        cells = ['id', 'name', 'sex', 'score', 'class_', 'course_id']
        rows_json = grid_json(page, total_paper, records, rows, 'id', cells)
        return rows_json


class GradeList(BaseManager):
    def get(self):
        params = request.args
        username = session.get('username')
        grade_info = models.Grade.query.filter_by(id=username)

        return render.grade_lists()

class GradeInput(BaseManager):
    def get(self):
        return render.grade_input()
    def post(self):
        params = request.form
        # student_numbers = params.get('course_numbers')
        course_numbers = params.get('course_numbers').split(',')
        course_names = params.get('course_names').split(',')
        course_scores = params.get('course_scores').split(',')
        course_results = params.get('course_results').split(',')

        for index,value in enumerate(course_numbers):
            print index, value

            if value:
                course = {
                    'student_c_name': course_names[index],
                    'student_c_score': int(course_scores[index]),
                    'student_c_number': course_numbers[index],
                    'student_c_result': course_results[index],
                    'semester': params.get('semester'),
                    'number': params.get('student_number'),
                    'college': params.get('college'),
                    'subject': params.get('subject'),
                    'student_class': params.get('student_class'),
                }
                print course
                courseinfo = models.GradeCourse(course).save()


                # value = {
            #     'student_c_number': [params.get('course_numbers').split(',')][i],
            # }
            # print value
        # course = {
        #     'student_c_name': params.get('course_names'),
        #     'student_c_score': int(params.get('course_scores')),
        #     'student_c_number': params.get('course_numbers'),
        #     'student_c_result': params.get("course_results"),
        #     'semester':params.get('semester'),
        #     'number':params.get('student_number'),
        #     'college': params.get('college'),
        #     'subject': params.get('subject'),
        #     'student_class': params.get('student_class'),
        # }

        user = {
            'college': params.get('college'),
            'subject': params.get('subject'),
            'student_class': params.get('student_class'),
            'student_name': params.get('student_name'),
            'student_number': params.get('student_number')
        }
        # print user
        # print course
        gradeuser = models.GradeUser(user).save()
        return success2json("ff")

app = Blueprint('grade_app', __name__, template_folder='templates')
app.add_url_rule('/input', view_func=GradeInput.as_view('grade_input'))
app.add_url_rule('/lists', view_func=GradeList.as_view('grade_lists'))
app.add_url_rule('/grid', view_func=GridGrade.as_view('grade_grid'))