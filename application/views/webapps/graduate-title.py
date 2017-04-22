#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session
from application.base import BaseManager, render_jinja
import json
from application.db import  models
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/graduate', encoding='utf-8',)

class CreateTitle(BaseManager):
    def get(self):
        return render.create_title()
    def post(self):
        params = request.form
        title =  params.get("t_name")
        type = params.get("t-type")
        status = params.get("t_status")
        values = {
            "title":title,
            "status":status,
            "type":type,
        }
        print "-----------",values
        return 'ok'