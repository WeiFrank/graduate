#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session
from application.base import BaseManager, render_jinja
import json
import  time
from sqlalchemy.sql import and_, or_
from datetime import datetime
from application.db import  models
import  jieba
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/graduate', encoding='utf-8',)
class GradeTitle(BaseManager):

        def get(self):
            params = request.args
            # print "##############",params.get('page')
            filters = {}
            panger = Pager()
            page, total_paper, records, rows = panger.grid_rows_query(params=params, table='titles', mode='count')
            cells = ['id', 'title_', 'type', 'status']
            rows_json = grid_json(page, total_paper, records, rows, 'id', cells)
            return rows_json
class ListTitle(BaseManager):
    def get(self):
        return render.title_list()

class TitleCreate(BaseManager):
    def get(self):
        return  render.create_title()
    def post(self):
        params = request.form
        # values = {}
        flag = params.get("flag", None)
        if flag:
            title = params.get("title_")
            type_ = params.get("type")
            t_from = params.get("t_from")
            author_id = params.get("author_id")
            values = {
                "title_": title,
                "type": type_,
                "author_id": author_id,
                "t_from": t_from,
                "student": session.get("name"),
                "status": u"已选中",
                "success_time":current_time
            }
            obj = models.Title.query.filter_by(student=session.get("name")).first()
            if obj:
                # print "eeeeeeeeeeeeeee"
                return exception2json("您已经选过,请勿多选")
        else:
            title = params.get("t_name")
            type = params.get("t_type")
            status = params.get("t_status")
            author = session.get("name")
            values = {
                "title_":title,
                "status":status,
                "type":type,
                "author_id": author,
            }
        print "-----------",values
        models.Title(values).save()
        return  success2json("success")

class TitleUpgate(BaseManager):
        def get(self):
            id = request.args.get("title_id")
            title = models.Title.query.filter_by(id=id).first()
            return render.update_title(title=title)

        def post(self):
            params = request.form
            id = params.get("id")
            obj = models.Title.query.filter_by(id=id).first()
            title = params.get("t_name")
            type_ = params.get("t_type")
            status = params.get("t_status")
            values = {
                "title_": title,
                "type": type_,
                "author_id": session.get("name"),
                "status":status
            }
            print "-----------", values
            obj.update(values)
            return success2json('ok')

class TitleDelete(BaseManager):
    def post(self):
        params = request.form
        title = models.Title.query.filter_by(id=params.get('id')).first()
        if not title:
            return exception2json("title is not exist")
        title.hard_delete()
        return success2json("ok")
class TitleChoice(BaseManager):
    def get(self):
        author_id = request.args.get("key_name")
        teacher = models.Title.query.filter_by(author_id=author_id).all()
        if teacher:
            return render.title_choice(teacher=teacher)
        else:
            return render.title_choice()
    def post(self):
        pass
current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


class TitleChange(BaseManager):
    def post(self):
        params = request.form
        id = params.get("id")
        print  "_________", id
        user_name = session.get("name")
        check = models.Title.query.filter_by(student=user_name).first()
        if check:
            return exception2json("请勿多选，只能选择一个")
        title_obj = models.Title.query.filter_by(id=id).first()
        print title_obj
        values = {
            "student":user_name,
            "status": u"已选中",
            "success_time":current_time
        }
        print "000000000000", values
        title_obj.update(values)
        return  success2json("选择课题成功")
class TitleLook(BaseManager):
    def get(self):
        teacher = session.get("name")
        # print "4444", teacher
        to = models.Title.query.filter(and_(models.Title.author_id == teacher, models.Title.student != '')).all()

        if to:
            return  render.title_look(teacher=to)
        else:
            return  render.title_look()
class TitleSuccess(BaseManager):
    def get(self):
        student = session.get("name")
        obj = models.Title.query.filter_by(student=student).first()
        if obj:
            return render.title_student(student=obj)
        else:
            return render.title_student(tip=u"您还未选择课题")
    def post(self):
        id = request.form.get("id")
        obj = models.Title.query.filter_by(id=id).first()
        if obj.t_from == u"自拟":
            obj.hard_delete()
        else:
            values = {
                "status":u"可选",
                "student":'',

            }
            obj.update(values)
        # obj.hard_delete()
        return success2json("删除成功")
class TitleFilter(BaseManager):
    def get(self):
        return render.title_filter()
    def post(self):
        param = request.form.get("t_name")
        obj  = Filter(param)
        f = obj.deal_filter()
        # print f
        if len(f) > 0:

            return render.title_filter(result=f)
        else:
            return  render.title_filter()
class Filter:
    def __init__(self, title):
        self.title = title
    def deal_filter(self):
        title_ = jieba.cut(self.title, cut_all=False)
        dest = []

        for t in title_:
            dest.append(t)
        # length = len(dest)
        # print "lllllllll", length
        obj = models.Title.query.all()
        if obj:
            r = []
            # count = 0
            for t in obj:
                result = {}

                org = []
                count = 0
                data = jieba.cut(t.title_, cut_all=False)
                print data
                for d in data:
                    print d
                    org.append(d)
                # print "----", t.title_
                for index, value in enumerate(dest):
                    if dest[index] in org:
                        count += 1
                        print count
                length = len(org)
                print "llllllllllll",length
                print "cccccccccccc", count
                sum_ = (float(count) / float(length)) * 100
                print "*******", sum_
                if sum_ >= int(50):
                    result["title"] = t.title_
                    result["student"] = t.student
                    result["rate"] = sum_
                    r.append(result)
            print "tttttttttt", r
            return r


app = Blueprint('title_app', __name__, template_folder='templates')
app.add_url_rule('/lists', view_func=ListTitle.as_view('title_lists'))
app.add_url_rule('/grid', view_func=GradeTitle.as_view('title_grid'))
app.add_url_rule('/create', view_func=TitleCreate.as_view('title_create'))
app.add_url_rule('/update', view_func=TitleUpgate.as_view('title_update'))
app.add_url_rule('/delete', view_func=TitleDelete.as_view('title_delete'))
app.add_url_rule('/choice', view_func=TitleChoice.as_view('title_choice'))
app.add_url_rule('/change', view_func=TitleChange.as_view('title_change'))
app.add_url_rule('/look', view_func=TitleLook.as_view('title_look'))
app.add_url_rule('/student', view_func=TitleSuccess.as_view('title_student'))
app.add_url_rule('/filter', view_func=TitleFilter.as_view('title_filter'))