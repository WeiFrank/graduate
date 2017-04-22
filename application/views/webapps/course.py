#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session
from application.base import BaseManager, render_jinja
import json
from application.db import  models
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/course', encoding='utf-8',)

class CourseList(BaseManager):
    def __init__(self):
        pass
    def get(self):
        return render.course_lists()

class GridCourse(BaseManager):
    def get(self):
        params = request.args
        # print "##############",params.get('page')
        filters = {}
        panger = Pager()
        page, total_paper, records, rows = panger.grid_rows_query(params=params, table='course', mode='count')
        cells = ['id', 'c_name', 'c_score', 'c_type', 'owner']
        rows_json = grid_json(page, total_paper, records, rows, 'id', cells)
        return rows_json
        # return json.dumps({'r':[{'c':['id']}]})

class CourseCreate(BaseManager):
    def __init__(self):
        pass
    def get(self):
        return  render.course_create()
    def post(self):
        params = request.form
        current_user = session.get('username', None)
        values = {
            'c_name': params.get('c_name'),
            'id': params.get('c_number'),
            'c_score': params.get('c_score'),
            'owner': current_user,

        }
        print "*************", values
        check_exist = models.Course.query.filter_by(id=params.get('c_number')).first()
        if check_exist is not None:
            return exception2json("name exist")
        course = models.Course(values).save()
        return success2json("create course success")

class CourseUpdate(BaseManager):
    def get(self):
        params = request.args

        course = models.Course.query.filter_by(id=params.get('course_id')).first()
        return render.course_update(course=course)
    def post(self):
        params = request.form

        course = models.Course.query.filter_by(id=params.get('id')).first()

        if not course:
            return exception2json("course is not exist")
        values = {
            'c_name': params.get('c_name'),
            'c_id':params.get('c_number'),
            'c_score':params.get('c_score')

        }


        course.update(values)

        return success2json("ooo")
class CourseDelete(BaseManager):
    def post(self):
        params = request.form
        course = models.Course.query.filter_by(id=params.get('id')).first()
        if not course:
            return exception2json("course is not exist")
        course.hard_delete()
        return success2json("ok")

class GradeInput(BaseManager):
    def get(self):
        c_owner = session.get('username', None)
        c_id = request.args.get('course_id')

        courses = models.Course.query.filter_by(id=c_id).first()

        return render.grade_input(courses=courses)
    def post(self):
        params = request.form
        owner = session.get('username',None)
        g_number = params.get("numbers").split(',')
        sex = params.get("sexs").split(',')
        name = params.get("names").split(',')
        score = params.get("scores").split(',')
        cnumber = params.get("cnumber")
        class_ = params.get("class_")
        semester = params.get("semester")
        c_type = params.get('c_type'),
        for index, value in enumerate(g_number):
            print "********", index,value
            if value:
                values ={
                "number":g_number[index],
                "sex": sex[index],
                "name":name[index],
                "score" :score[index],
                "course_id":cnumber,
                "class_":class_,
                "owner":owner,
                "semester":semester
                }
                print "------------" ,values
                models.Grade(values).save()
                # course = models.Course.query.filter_by(id=cnumber).first()



        return success2json("grade success")
app = Blueprint('course_app', __name__, template_folder='templates')
app.add_url_rule('/lists', view_func=CourseList.as_view('course_lists'))
app.add_url_rule('/create', view_func=CourseCreate.as_view('course_create'))
app.add_url_rule('/update', view_func=CourseUpdate.as_view('course_update'))
app.add_url_rule('/delete', view_func=CourseDelete.as_view('course_delete'))
app.add_url_rule('/input', view_func=GradeInput.as_view('grade_input'))

app.add_url_rule('/grid', view_func=GridCourse.as_view('course_grid'))
