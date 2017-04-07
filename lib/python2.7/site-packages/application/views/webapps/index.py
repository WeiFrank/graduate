from flask import request, Blueprint,redirect
from application.db import models
from application.base import BaseManager, render_jinja
render = render_jinja('static/templates', encoding='utf-8')

class Home(BaseManager):
    def __init__(self):
        pass
    def get(self):
        return render.home()
    def post(self):
        return render.home()

class Login(BaseManager):
    def get(self):
        return render.user_login(tip='')

    def post(self):
        params = request.form
        username = params.get('username', '')
        password = params.get('password', '')
        identity = params.get('identity', '')
        if identity == 'student':
            print "----------", identity
            check_user = models.UserStudent.query.filter_by(student_number=username).first()
            check_password = models.UserStudent.query.filter_by(password=password).first()
            if check_user:
                if check_password:
                    return redirect('/home')
            else:
                return exception2json("user not exist")
        elif identity == 'teacher':
            check_user = models.UserTeacher.query.filter_by(teacher_number=username).first()
            check_password = models.UserTeacher.query.filter_by(password=password).first()
            if check_user:
                if check_password:
                    return redirect('/home')
            else:
                return exception2json("user is not exist")
        else:
            return render.user_login(tip="erong")


app = Blueprint('login_home', __name__, template_folder='templates')
app.add_url_rule('/home', view_func=Home.as_view('home'))
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/', view_func=Login.as_view('login_another'))