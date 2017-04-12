#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session,redirect
from application.base import BaseManager, render_jinja
from application.db import models
from application.utils.query import Pager, success2json,exception2json

render = render_jinja('static/templates/course', encoding='utf-8',)

class LeaveList(BaseManager):
    def __init__(self):
        pass
    def get(self):
        return render.leave_lists()

class GridLeave(BaseManager):
    def get(self):
        params = request.args
        # print "##############",params.get('page')
        filters = {}
        panger = Pager()
        page, total_paper, records, rows = panger.grid_rows_query(params=params, table='course', mode='count')
        cells = ['id', 'name', 'start_date', 'end_date','description','status']
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

        values = {
            "c_name": params.get('c_name'),
            "c_score":params.get('c_score'),
            "c_number":params.get('c_number'),
        }

        check_exist = models.Course.query.filter_by(c_name=params.get('c_name')).first()
        if check_exist is not None:
            return exception2json("name exist")
        course = models.Course(values).save()
        return success2json(course)

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
            'c_number':params.get('c_number'),
            'c_score':params.get('c_score')
        }
        # update_values(values, 'c_name', params.get('c_name'))
        # update_values(values, 'c_number', params.get('c_number'))
        # update_values(values, 'c_score', params.get('c_score'))
        course.update(values)

        return success2json(course)
class CourseDelete(BaseManager):
    def post(self):
        params = request.form
        course = models.Course.query.filter_by(id=params.get('id')).first()
        if not course:
            return exception2json("course is not exist")
        course.hard_delete()
        return success2json(course)