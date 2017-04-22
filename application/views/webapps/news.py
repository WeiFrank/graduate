#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session
from application.base import BaseManager, render_jinja
import json
from application.db import  models
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/news', encoding='utf-8',)

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
        obj = models.News.query.all()
        return render.new_list(obj=obj)
#
class NewDetail(BaseManager):
    def get(self):
        id = request.args.get("nid", None)
        obj = models.News.query.filter_by(id=id).first()
        return render.new_detail(obj=obj)

app = Blueprint('new_app', __name__, template_folder='templates')
app.add_url_rule('/create', view_func=NewCreate.as_view('new_create'))
app.add_url_rule('/look', view_func=NewList.as_view('new_look'))
app.add_url_rule('/detail', view_func=NewDetail.as_view('new_detail'))