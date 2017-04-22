#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session
from application.base import BaseManager, render_jinja
import json
from application.db import  models
from sqlalchemy.sql import and_, or_
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/calculation', encoding='utf-8',)

class CalculationList(BaseManager):
    # def get(self):
    #     return render.calculation_lists()
    def get(self):

        result = []

        paramas = request.args
        class_ = paramas.get("class_")
        s = paramas.get("semester")
        obj = Clculation(class_, s)
        result = obj.deal_cal()
        if result:
            return render.calculation_lists(results=result, class_=class_, semester=s)
        else:
            return render.calculation_lists()

class Clculation:

    def __init__(self, class_, s):
        self.class_ =class_
        self.s = s

    def deal_cal(self):
        result = []
        if self.class_ and self.s:
            grades = models.Grade.query.filter(and_(models.Grade.class_ == self.class_, models.Grade.semester == self.s)).all()
            for grade in grades:
                grade_score = 0
                grade_sum = 0
                obj = {}
                c_obj = json.loads(grade.detail)

                for k,v in c_obj.iteritems():
                    if k in ['semester', 'name', 'class_']:
                        continue
                    if int(v['grade']) == 0:
                        continue
                    # print k, v
                    # print  c_obj[k]['grade']
                    grade_sum += (float(c_obj[k]['grade']) - 50) * float(c_obj[k]['score'])
                    grade_score += float(c_obj[k]['score'])
                # print grade_score
                # print grade_sum

                grade_point = grade_sum / (grade_score*10)
                obj['name'] = grade.name
                obj['point'] = "%.2f" % grade_point
                result.append(obj)
            print "*************",result
            return  result

app = Blueprint('gradecal_app', __name__, template_folder='templates')
app.add_url_rule('/lists', view_func=CalculationList.as_view('cal_lists'))