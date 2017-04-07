from flask import Blueprint, request
from application.base import BaseManager, render_jinja

from application.db import  models

from application.utils.query import Pager, success2json,exception2json,\
    grid_json
render = render_jinja('static/templates/xueji', encoding='utf-8',)

class XueJiList(BaseManager):
    def __init__(self):
        pass
    def get(self):
        return render.xueJi_lists()

class GridXueJi(BaseManager):
    def get(self):
        params = request.args
        # print "##############",params.get('page')
        filters = {}
        panger = Pager()
        page, total_paper, records, rows = panger.grid_rows_query(params=params, table='xueJi', mode='count')
        cells = ['id', 'c_name', 'c_number', 'c_score']
        rows_json = grid_json(page, total_paper, records, rows, 'id', cells)
        return rows_json
        # return json.dumps({'r':[{'c':['id']}]})

class XueJiCreate(BaseManager):
    def __init__(self):
        pass
    def get(self):
        return  render.xueJi_create()
    def post(self):
        params = request.form
        # print "---------", dir(params)
        values = {

            'student_num':params.get('student_num'),
            'change_date':params.get('change_date'),
            'change_num':params.get('change_num'),
            'change_type': params.get('change_type'),
            'change_description': params.get('change_description'),
            'recover_date': params.get('recover_date'),
            's_department': params.get('s_department'),
            's_subject': params.get('s_subject'),
            's_class':params.get('s_class'),
            's_plan':params.get('s_plan')
        }

        check_exist = models.XueJiChange.query.filter_by(c_name=params.get('c_name')).first()
        if check_exist is not None:
            return exception2json("name exist")
        xueji = models.XueJiChange(values).save()
        return success2json(xueJi)

class XueJiUpdate(BaseManager):
    def get(self):
        params = request.args

        # xueJi = models.XueJiChange.query.filter_by(id=params.get('xueJi_id')).first()
        return render.XueJi_update()
    def post(self):
        params = request.form

        xueJi = models.XXueJiChange.query.filter_by(id=params.get('id')).first()

        if not xueJi:
            return exception2json("XueJi is not exist")
        values = {
            'student_num':params.get('student_num'),
            'change_date':params.get('change_date'),
            'change_num':params.get('change_num'),
            'change_type': params.get('change_type'),
            'change_description': params.get('change_description'),
            'recover_date': params.get('recover_date'),
            's_department': params.get('s_department'),
            's_subject': params.get('s_subject'),
            's_class':params.get('s_class'),
            's_plan':params.get('s_plan')
        }
        # update_values(values, 'c_name', params.get('c_name'))
        # update_values(values, 'c_number', params.get('c_number'))
        # update_values(values, 'c_score', params.get('c_score'))
        XueJi.update(values)

        return success2json(XueJi)
class XueJiDelete(BaseManager):
    def post(self):
        params = request.form
        xueji = models.XueJiChange.query.filter_by(id=params.get('id')).first()
        if not pool:
            return exception2json("XueJi is not exist")
        xueji.hard_delete()
        return success2json(xueji)
app = Blueprint('xueji_app', __name__, template_folder='templates')
app.add_url_rule('/lists', view_func=XueJiList.as_view('XueJi_lists'))
app.add_url_rule('/create', view_func=XueJiCreate.as_view('XueJi_create'))
app.add_url_rule('/update', view_func=XueJiUpdate.as_view('XueJi_update'))
app.add_url_rule('/delete', view_func=XueJiDelete.as_view('XueJi_delete'))

app.add_url_rule('/grid', view_func=GridXueJi.as_view('XueJi_grid'))