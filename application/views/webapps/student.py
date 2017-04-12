from flask import Blueprint, request
from application.base import BaseManager, render_jinja
import json
from application.db import  models
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/base', encoding='utf-8',)

class StudentList(BaseManager):
    def __init__(self):
        pass
    def get(self):
        params = request.args
        print 'rrrrrrrrrrrrrrr', params.get('subject')
        return render.student_lists()

class GridStudent(BaseManager):
    def get(self):
        params = request.args
        # print "##############",params.get('page')
        filters = {}
        panger = Pager()
        page, total_paper, records, rows = panger.grid_rows_query(params=params, table='student', mode='count')
        cells = ['id', 's_number', 's_name', 's_sex', 's_id', 's_telphone', 's_political']
        rows_json = grid_json(page, total_paper, records, rows, 'id', cells)
        return rows_json




class StudentCreate(BaseManager):
    def get(self):
        params = request.args
        classes = models.Class.query.all()

        return render.student_create(classes=classes)
    def post(self):
        params = request.form
        # "s_political":params.get('s_political'),
        # "admission_time":params.get('admission_time'),
        # "class_id": params.get('class_id'),
        values = {
            "s_name": params.get('s_name'),
            "s_e_mail": params.get('s_e_mail'),
            "s_number": params.get('s_number'),
            "class_id": params.get('class_id'),
            "s_sex": params.get('s_sex'),
            "s_job":params.get('s_job'),
           "s_political":params.get('s_political'),

            "s_telphone":params.get('s_telphone'),

        }


        print "@@@@@@@@@@@@@@@@", values

        check_exist = models.Student.query.filter_by(s_number=params.get('s_number')).first()

        if check_exist is not None:
            return exception2json("student exist")
        student = models.Student(values).save()
        return success2json(student)
class StudentDelete(BaseManager):
    def post(self):
        params = request.form
        student = models.Student.query.filter_by(id=params.get('id')).first()
        if not student:
            return exception2json("course is not exist")
        student.hard_delete()
        return success2json(student)
class StudentUpdate(BaseManager):
    def get(self):
        params = request.args
        print "---------",params.get('student_id')
        student = models.Student.query.filter_by(id=params.get('student_id')).first()
        classes = models.Class.query.all()
        return render.student_update(student=student,classes=classes)

    def post(self):
        params = request.form
        student = models.Student.query.filter_by(id=params.get('id')).first()
        if not student:
            return exception2json("student is not exist")
        print "id---------", params.get('class_id')
        values = {
            "s_name": params.get('s_name'),
            "s_e_mail": params.get('s_e_mail'),
            "s_number": params.get('s_number'),
            "class_id": params.get('class_id'),
            "s_sex": params.get('s_sex'),
            "s_job": params.get('s_job'),
            "s_political": params.get('s_political'),
            "s_telphone": params.get('s_telphone'),
            "admission_time": params.get('admission_time'),
        }
        student.update(values)

        return success2json(student)
app = Blueprint('base_app', __name__, template_folder='templates')
app.add_url_rule('/lists', view_func=StudentList.as_view('base_lists'))
app.add_url_rule('/create', view_func=StudentCreate.as_view('base_create'))
app.add_url_rule('/update', view_func=StudentUpdate.as_view('base_update'))
app.add_url_rule('/delete', view_func=StudentDelete.as_view('base_delete'))

app.add_url_rule('/grid', view_func=GridStudent.as_view('base_grid'))