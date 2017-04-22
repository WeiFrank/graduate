from flask import Blueprint, request
from application.base import BaseManager, render_jinja
import json
from application.db import  models
from sqlalchemy.sql import and_, or_
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/class', encoding='utf-8',)

class ClassList(BaseManager):
    def __init__(self):
        pass
    def get(self):
        return render.class_lists()

class GridClass(BaseManager):
    def get(self):
        params = request.args
        all = models.Class.query.all()

        filters = {}
        panger = Pager()
        page, total_paper, records, rows = panger.grid_rows_query(params=params, table='class', mode='count')
        cells = ['id', 'name', 'students_num']
        rows_json = grid_json(page, total_paper, records, rows, 'id', cells)
        return rows_json
class ClassCreate(BaseManager):
    def get(self):
        params = request.args
        return render.class_create()
    def post(self):
        params = request.form
        # "s_political":params.get('s_political'),
        # "admission_time":params.get('admission_time'),
        # "class_id": params.get('class_id'),

        values = {
            "name": params.get('name'),
        }

        check_exist = models.Class.query.filter_by(name=params.get('name')).first()

        if check_exist is not None:
            return exception2json("Class exist")
        classes = models.Class(values).save()
        return success2json(classes)
class ClassDelete(BaseManager):
    def post(self):
        params = request.form
        classes = models.Class.query.filter_by(id=params.get('id')).first()
        if not classes:
            return exception2json("class is not exist")
        Class.hard_delete()
        return success2json(Class)
class ClassUpdate(BaseManager):
    def get(self):
        params = request.args
        print "---------",params.get('class_id')
        classes = models.Class.query.filter_by(id=params.get('class_id')).first()
        return render.class_update(classes=classes)

    def post(self):
        params = request.form
        classes = models.Class.query.filter_by(id=params.get('id')).first()
        if not classes:
            return exception2json("Class is not exist")
        values = {
            "name": params.get('name'),
        }
        classes.update(values)

        return success2json(classes)

class ClassGrade(BaseManager):
    def get(self):
        params = request.args
        # class_ =  params.get("key_class")
        # semester = params.get("key_semester")
        # if class_ and semester:
        c_obj = models.Grade.query.filter(and_(models.Grade.class_ == '131', models.Grade.semester == '2013-2014'))
        for key in c_obj:
            c = json.loads(key.detail)
            print "-----------",c
        return  "ok"

app = Blueprint('class_app', __name__, template_folder='templates')
app.add_url_rule('/look', view_func=ClassGrade.as_view('class_lists'))
app.add_url_rule('/create', view_func=ClassCreate.as_view('class_create'))
app.add_url_rule('/update', view_func=ClassUpdate.as_view('class_update'))
app.add_url_rule('/delete', view_func=ClassDelete.as_view('class_delete'))

app.add_url_rule('/grid', view_func=GridClass.as_view('clas_grid'))