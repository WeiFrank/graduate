import  os
current_path = os.path.abspath(os.path.split(os.path.realpath(__file__))[0])

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

conf = '%s/%s' % (current_path, 'configure_file')

import  ConfigParser

app = Flask(__name__)
db = SQLAlchemy()
# print conf

def database_url():
    parse = ConfigParser.ConfigParser()
    parse.read(conf)
    server = parse.get('mysql', 'server')
    user = parse.get('mysql', 'user')
    password = parse.get('mysql', 'password')
    host = parse.get('mysql', 'host')
    port = parse.get('mysql', 'port')
    database = parse.get('mysql', 'database')
    return  "%s://%s:%s@%s:%s/%s" % (server, user, password, host, port, database)

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url()
    app.config['SECRET_KEY'] = 'qdjoqwifjjfj'
    app.config['SSL_DISABLE'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_RECORD_QUERIES'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    from views.webapps import (
    user,
    index,
    score,
    course,
    modal,
    student,
    classes,
    xueji,
    courage,
    grade,
    )

    # app.register_blueprint(student.app, url_prefix='/student')
    app.register_blueprint(user.app, url_prefix='/user')
    app.register_blueprint(score.app, url_prefix='/score')
    app.register_blueprint(course.app, url_prefix='/course')
    app.register_blueprint(modal.app, url_prefix='/confirm_modal')
    app.register_blueprint(student.app, url_prefix='/student')
    app.register_blueprint(classes.app, url_prefix='/class')
    app.register_blueprint(xueji.app, url_prefix='/xueji')
    app.register_blueprint(courage.app, url_prefix='/courage')
    app.register_blueprint(grade.app, url_prefix='/grade')

    app.register_blueprint(index.app, url_prefix='')
    #app.register_blueprint(index.app, url_prefix='/home')
    # app.register_blueprint(school.app, url_prefix='/school')
    # app.register_blueprint(college.app, url_prefix='/college')
    # app.register_blueprint(subject.app, url_prefix='/subject')

    return app, db

if __name__ == '__main__':
    pass
    #database_url()
    # print  server
    # print  host
    # print  database
    # print  user
    # print  port