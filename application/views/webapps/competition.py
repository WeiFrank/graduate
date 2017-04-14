#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session
from application.base import BaseManager, render_jinja
import json
from application.db import  models
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/honer', encoding='utf-8',)

class CompetitionAdd(BaseManager):
    def get(self):

        return render.competition_add()
    def post(self):
        pass

class CompetitionDelete(BaseManager):
    def get(self):
        pass


