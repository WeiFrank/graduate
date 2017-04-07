from flask import Blueprint, request
from application.base import BaseManager, render_jinja

from application.db import  models

from application.utils.query import Pager, success2json,exception2json,\
    grid_json
render = render_jinja('static/templates/courage', encoding='utf-8',)


class CourageList(BaseManager):
    def get(self):
        return  render.courage_lists()

app = Blueprint('courage_app', __name__, template_folder='templates')
app.add_url_rule('/lists', view_func=CourageList.as_view('courage_lists'))