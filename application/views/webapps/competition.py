#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session
from application.base import BaseManager, render_jinja
import json
from application.db import  models
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/competition', encoding='utf-8',)

class GridCompetition(BaseManager):
    def get(self):
        params = request.args
        # print "##############",params.get('page')
        filters = {}
        panger = Pager()
        page, total_paper, records, rows = panger.grid_rows_query(params=params, table='competition', mode='count')
        cells = ['id','name','class_', 'title', 'team_members', '_datw', 'level','competition_type']
        rows_json = grid_json(page, total_paper, records, rows, 'id', cells)
        return rows_json
class CompetitionList(BaseManager):
    def get(self):
        print "ooooooooooooo"
        return render.competition_lists()

class CompetitionAdd(BaseManager):
    def get(self):
        return  render.competition_add()

    def post(self):
        params = request.form
        values = {
            "team_members":params.get("members"),
            "title":params.get("title"),
            "competition_type":params.get("type"),
            "level":params.get("level")
            # "_date":params.get("time"),
        }
        print "-----------", values
        models.Competition(values).save()
        return success2json("create com ok")
class CompetitionDelete(BaseManager):
    def post(self):
        id = request.form.get("id")
        competition = models.Competition.query.filter_by(id=id).first()
        if not competition:
            return  exception2json("not")
        competition.hard_delete()
        return  success2json("ok")
class CompetitionUpdate(BaseManager):
    def get(self):
        competition_id = request.args.get("competition_id")
        competition = models.Competition.query.filter_by(id=competition_id).first()
        return  render.competition_update(competition=competition)
    def post(self):
       params = request.form
       id = params.get("id")
       competition = models.Competition.query.filter_by(id=id).first()
       values = {
           "team_members": params.get("members"),
           "title": params.get("title"),
           "competition_type": params.get("type"),
           "level": params.get("level"),
           "name": params.get("name"),
           "class_":params.get("class_"),

       }
       competition.update(values)
       return  success2json("update ok")



app = Blueprint('competition_app', __name__, template_folder='templates')
app.add_url_rule('/lists', view_func=CompetitionList.as_view('competition_addbutons'))
app.add_url_rule('/add', view_func=CompetitionAdd.as_view('competition_add'))
app.add_url_rule('/delete', view_func=CompetitionDelete.as_view('competition_delete'))

app.add_url_rule('/grid', view_func=GridCompetition.as_view('competition_grid'))
app.add_url_rule('/update', view_func=CompetitionUpdate.as_view('competition_update'))
