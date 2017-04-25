#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session,render_template
from application.base import BaseManager, render_jinja
import json
from sqlalchemy.sql import and_, or_
from application.db import  models
import  datetime
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/news', encoding='utf-8',)
def current_time():
    return  datetime.datetime.now()
def todays():
    return datetime.datetime.now()-datetime.timedelta(2)
class NewCreate(BaseManager):
    def get(self):
        return  render.new_create()
    def post(self):
        params = request.form
        title = params.get("title")
        author = params.get("author")
        content = params.get("content")
        values = {
            "title":title,
            "publisher":author,
            "content":content,
        }
        models.News(values).save()
        return success2json("消息发布成功")
class NewList(BaseManager):
    def get(self):
        page = request.args.get('page', 1, type=int)
        lasted = []
        obj = models.News.query
        paginate = obj.paginate(page=page, per_page=6)  # 默认每页10条内容
        all = models.News.query.all()
        if all:
            for n in all:
                print  n.created_at
                print current_time()
                print todays()
                if n.created_at > todays() and n.created_at < current_time():
                    print "ddddddddddddd"
                    lasted.append(n)
                else:
                    continue
        # lasted = models.News.query.filter(and_(todays()< models.News.created_at,models.News.created_at<current_time() )).all()
        print "llllllllllll", lasted
        if paginate:
            return render_template("news/new_list.html", pagination=paginate, lasted=lasted)
        else:
            return  render_template("news/new_list.html")
class NewDetail(BaseManager):
    def get(self):
        id = request.args.get("nid", None)
        obj = models.News.query.filter_by(id=id).first()
        return render.new_detail(obj=obj)

app = Blueprint('new_app', __name__, template_folder='templates')
app.add_url_rule('/create', view_func=NewCreate.as_view('new_create'))
app.add_url_rule('/look', view_func=NewList.as_view('new_look'))
app.add_url_rule('/detail', view_func=NewDetail.as_view('new_detail'))