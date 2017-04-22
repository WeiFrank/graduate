#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session,redirect
from application.base import BaseManager, render_jinja
from application.db import models
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
import  os
from xlrd import open_workbook
from collections import OrderedDict
from application.apps import app as app_
import  json
render = render_jinja('static/templates/grade', encoding='utf-8',)
UPLOAD_FOLDER = '/root/desigine/studentinfomanager/application/static/upload'





class DealTable(object):
    def __init__(self,file_grade=None, course_col_start=None, course_col_end=None, table_row_start=None, table_row_end=None,
                 college=None, subject=None, class_=None, semester=None, name_col=1, number_col=4):

        self.course_col_start = course_col_start
        self.course_col_end = course_col_end
        self.table_row_start = table_row_start
        self.table_row_end = table_row_end
        self.college = college
        self.subject = subject
        self.class_ = class_
        self.semester = semester
        self.name_col = name_col
        self.number_col = number_col
        self.file = file_grade


        # info = {}

        print  self.table_row_end

    def read_file(self):
        data = open_workbook(os.path.join(UPLOAD_FOLDER, self.file))
        table = data.sheets()[0]
        return  table
    def deal_score(self):
        course = {}
        table = self.read_file()
        # row scan
        for row in range(self.table_row_start, self.table_row_end):
            # course = {}
            for col in range(self.course_col_start, self.course_col_end):


                subd = course[table.col_values(col)[0]] = {}
                # print course
                subd['number'] = table.row_values(self.table_row_start - 4)[col]
                subd['type'] = table.row_values(self.table_row_start - 3)[col]
                subd['score'] = table.row_values(self.table_row_start - 2)[col]

                course[table.col_values(col)[0]]['grade'] = table.row_values(row)[col]
                # info['number'] = table.row_values(row)[self.p_col_start - 4]
                # info['name'] = table.row_values(row)[self.p_col_start - 1]
                # course.update(info)

            name = table.row_values(row)[self.course_col_start - self.name_col]
            number = table.row_values(row)[self.course_col_start - self.number_col]
            # print course
                    # print table.row_values(row)[self.p_col_start-4],table.row_values(row)[self.p_col_start-1]
            values = {
                "college": self.college,
                "subject": self.subject,
                'class_': self.class_,
                "semester": self.semester,
                "number":number,
                "name":name,
                'detail': json.dumps(course),
            }
            models.Grade(values).save()

        # os.remove(os.path.join(UPLOAD_FOLDER, self.file))



class GridGrade(BaseManager):
    def get(self):
        params = request.args
        # print "##############",params.get('page')
        filters = {}
        panger = Pager()
        page, total_paper, records, rows = panger.grid_rows_query(params=params, table='grade', mode='count')

        cells = ['number', 'name', 'sex', 'score', 'class_', 'course_id']
        rows_json = grid_json(page, total_paper, records, rows, 'id', cells)
        return rows_json


class GradeList(BaseManager):
    def get(self):
        params = request.args
        username = session.get('username')
        grade_info = models.Grade.query.filter_by(id=username)

        return render.grade_lists()


class GradeDelete(BaseManager):
    def post(self):
        params = request.form
        grade = models.Grade.query.filter_by(id=params.get('id')).first()
        if not grade:
            return exception2json("course is not exist")
        grade.hard_delete()
        return success2json("ok")

class GradeUpdate(BaseManager):
    def get(self):
        params = request.args
        print "----------", params.get("grade_id")
        gradeobj = models.Grade.query.filter_by(id=params.get('grade_id')).first()
        print "******",    gradeobj.id
        return render.grade_update(gradeobj=gradeobj)
    def post(self):
        params = request.form
        grade = models.Grade.query.filter_by(id=params.get('id')).first()

        id = params.get("number")
        sex = params.get("sex")
        name = params.get("name")
        score = params.get("score")

        class_ = params.get("class_")
        semester = params.get("semester")
        values ={
            "number":id,
            "sex": sex,
            "name":name,
            "score" :score,
            "class_":class_,
            "semester":semester
        }
        print "------------" ,values
        grade.update(values)
        return success2json("grade success")
class FileUPload(BaseManager):
    def get(self):
        return render.grade_upload()
class GradeDeal(BaseManager):
    def post(self):
        file = request.files['file']
        params = request.form
        course_col_start = int(params.get("course_col_start"))
        course_col_end = int(params.get("course_col_end"))
        table_row_start = int(params.get("table_row_start"))
        table_row_end = int(params.get("table_row_end"))
        name_offset = int(params.get("name_offset"))
        number_offset = int(params.get("number_offset"))
        college = params.get("college")
        subject = params.get("subject")
        class_ = params.get("class_")
        semester = params.get("semester")
        print course_col_start, course_col_end
        print table_row_start, table_row_end
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        file_grade = os.path.join(UPLOAD_FOLDER, filename)

        # file_url = url_for('uploaded_file', filename=filename)
        t = DealTable(file_grade, course_col_start, course_col_end, table_row_start,
                      table_row_end, college, subject,class_,  semester, name_offset,number_offset)
        t.deal_score()

        return  'ok'

app = Blueprint('grade_app', __name__, template_folder='templates')
app.add_url_rule('/upload', view_func=FileUPload.as_view('grade_upload'))
app.add_url_rule('/lists', view_func=GradeList.as_view('grade_lists'))
app.add_url_rule('/grid', view_func=GridGrade.as_view('grade_grid'))
app.add_url_rule('/delete', view_func=GradeDelete.as_view('grade_delete'))
app.add_url_rule('/deal', view_func=GradeDeal.as_view('grade_input'))