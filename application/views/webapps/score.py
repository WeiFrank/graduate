from flask import Blueprint, request, session
from application.base import BaseManager, render_jinja

render = render_jinja('static/templates/score', encoding='utf-8',)

class ScoreList(BaseManager):
    def __init__(self):
        pass
    def get(self):
        return render.score_create()
    def post(self):
        return render.score_create()

app = Blueprint('scorecreate', __name__, template_folder='templates')
app.add_url_rule('/list', view_func=ScoreList.as_view('score_list'))
#app.add_url_rule('/teacher/create', view_func=TeacherCreate.as_view('teacher_create'))