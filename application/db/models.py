#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import  traceback
from application.apps import db
from sqlalchemy.exc import IntegrityError
from session import get_session
from datetime import datetime

def get_current_time():
    return datetime.now()
class ORMMethodBase(object):

    def __init__(self, kw_dict={}, *arg, **kw):
        print  'kkkkkkkkkkkkk', kw_dict
        for name, value in kw_dict.iteritems():
            print name, value
            setattr(self, name, value)

    def update(self, values, session=None):
        for k, v in values.iteritems():
            setattr(self, k, v)
        self.save(session=session)

    def save(self, session=None):
        if session is None:
            session = get_session()
        session.add(self)
        print '666666666'
        try:
            session.commit()
            # session.flush()
        except IntegrityError, e:
            print '#' * 100
            traceback.print_exc()
            session.rollback()
            print '#' * 100
            #db_utils.reraise(sys.exc_info(), 'after session rollback')
        return self

    def delete(self, session=None):
        self.update({'deleted': 1, 'deleted_at': db_utils.todaynow(), 'deleted_friend': self.id})
        return True

    def hard_delete(self, session=None):
        if session is None:
            session = get_session()

        session.delete(self)
        session.commit()
        return True


class Base(ORMMethodBase):
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    __table_initialized__ = False

    #id = db.Column(db.Integer, primary_key=True)
    deleted_at = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)

# class BaseA:
#     __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
#     __table_initialized__ = False
#     # admission_time = db.Column(db.DateTime)
#     semester = db.Column(db.DateTime)


#
# class Root(Base, db.Model):
#     __tablename__ = "root"
#     __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     password = db.Column(db.String(255))




# class Class(Base, db.Model):
#     __tablename__ = "class"
#     __table_args__ = (db.UniqueConstraint("name", ),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     # class_ = db.Column(db.String(255))
#     students = db.relationship('Student', backref=db.backref('class', order_by=id),
#                         primaryjoin='and_(Class.id == User.class_id,)')

    # @property
    # def students_num(self):
    #     return len(self.students)
class SchoolInfo:
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    __table_initialized__ = False
    college = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    e_mail = db.Column(db.String(255))
    telphone = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.Integer)
#
# class Teacher(Base,SchoolInfo, BaseA, db.Model):
#     __tablename__ = "teacher"
#     __table_args__ = (db.UniqueConstraint("teacher_number", ),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#     id = db.Column(db.Integer, primary_key=True)
#     teacher_number = db.Column(db.String(255))
#     identity = db.Column(db.String(255))
#
#
class Student(Base, SchoolInfo, db.Model):
    __tablename__ = "student"
    __table_args__ = (db.UniqueConstraint("student_number", ),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    # class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=True)
    xuejichange_id = db.Column(db.Integer, db.ForeignKey('xuejichange.id'), nullable=True)
    political_info = db.Column(db.String(255))
    student_job = db.Column(db.String(255))
    student_number = db.Column(db.String(255))
    class_ = db.Column(db.String(255))

class Role(Base, db.Model):
    __tablename__ = "role"
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    # users = db.relationship('User', backref=db.backref('role', order_by=id),
    #                     primaryjoin='and_(Role.id == User.role_id,)')
    user_admin = db.Column(db.String(255))

class User(Base, db.Model):
    __tablename__ = "users"
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    class_ = db.Column(db.String(255))
    admission = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    college = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    semester = db.Column(db.String(255))
    mail = db.Column(db.String(255))


class XueJiChange(Base, db.Model):
    __tablename__ = "xuejichange"
    __table_args__ = (db.UniqueConstraint("student_num", ),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.String(255))
    change_date = db.Column(db.DateTime)
    change_num = db.Column(db.Integer)
    change_type = db.Column(db.String(255))
    change_description = db.Column(db.Text)
    recover_date = db.Column(db.DateTime)
    s_department = db.Column(db.String(255))
    s_subject = db.Column(db.String(255))
    s_class = db.Column(db.String(255))
    s_plan = db.Column(db.String(255))

# gc = db.Table('gc',
#     db.Column('c_id', db.Integer, db.ForeignKey('course.id')),
#     db.Column('g_id', db.Integer, db.ForeignKey('grade.id'))
#     )

class Course(Base, db.Model):
    __tablename__ = "course"
    __table_args__ = (db.UniqueConstraint("c_name", ),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.String(40), primary_key=True)
    c_name = db.Column(db.String(255))
    c_score = db.Column(db.Integer)
    owner = db.Column(db.String(255))
    c_semester = db.Column(db.String(255))
    c_type = db.Column(db.String(255))
    grades = db.relationship("Grade", backref=db.backref('course', order_by=id),
            primaryjoin='and_(Course.id == Grade.course_id,)')


class Grade(Base,  db.Model):
    __tablename__ = "grade"
    __table_args__ = (
                     {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(255))
    name = db.Column(db.String(255))
    score = db.Column(db.String(255))
    class_ = db.Column(db.String(255))
    owner = db.Column(db.String(255))
    course_id = db.Column(db.ForeignKey('course.id'))


class GradeUser(Base, db.Model):
    __tablename__ = "grade_user"
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(255))
    studnet_number = db.Column(db.String(255))
    college = db.Column(db.String(255))
    subject = db.Column(db.String(255))

    student_class = db.Column(db.String(255))


class GradeCourse(Base, db.Model):
    __tablename__ = "grade_course"
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    student_c_name = db.Column(db.String(255))
    student_c_score = db.Column(db.Integer)
    student_c_number = db.Column(db.String(255))
    student_c_result = db.Column(db.Integer)
    number = db.Column(db.String(255))
    semester = db.Column(db.Integer)
    college = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    student_class = db.Column(db.String(255))

# class Honer(Base, db.Model):
#     __tablename__ = "honer"
#     __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#     id = db.Column(db.String(100), primary_key=True)
#     mane = db.Column(db.String(255))
#     start_date = db.Column(db.DateTime)
#     description = db.Column(db.Text)
#     people = db.Column(db.String(255))

class Competition(Base,db.Model):
    __tablename__ = "competition"
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.String(100), primary_key=True)
    team_leader = db.Column(db.String(255))
    team_member_one = db.Column(db.String(255))
    team_member_two = db.Column(db.String(255))
    title = db.Column(db.String(255))
    competition_type = db.Column(db.String(255))
    level = db.Column(db.String(255))
    source_date = db.Column(db.DateTime)
    ent_date = db.Column(db.DateTime)
    upload_owner = db.Column(db.String(255))

class Hanging(Base,db.Model):
    __tablename__ = "hanging"
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255))
    name = db.Column(db.String(255))
    class_ = db.Column(db.String(255))
    course = db.Column(db.String(255))
    status = db.Column(db.String(255))
    description = db.Column(db.String(255))
    uploader = db.Column(db.String(255))

class LeaveApply(Base, db.Model):
    __tablename__ = "leaveapply"
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    status = db.Column(db.String(255))
    apply_people = db.Column(db.String(255))




class Question(Base, db.Model):

    __tablename__ = 'questions'
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text(1024))
    answers_count = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime,default=get_current_time)

    author_id = db.Column(db.String(100), db.ForeignKey("users.id", ondelete="CASCADE"))
    author = db.relationship("User", backref=db.backref(
                            "questions", lazy="dynamic"), uselist=False)


class Answer(Base, db.Model):

    __tablename__ = 'answers'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(1024))
    comments_count = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime,default=get_current_time)

    author_id = db.Column(db.String(100), db.ForeignKey("users.id", ondelete="CASCADE"))
    author = db.relationship("User", backref=db.backref(
                            "answers", lazy="dynamic"), uselist=False)

    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    question = db.relationship("Question", backref=db.backref(
                            "answers", lazy="dynamic"), uselist=False)


class Comment(Base, db.Model):

    __tablename__ = 'comments'
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(1024))
    create_time = db.Column(db.DateTime,default=get_current_time)

    author_id = db.Column(db.String(100), db.ForeignKey("users.id", ondelete="CASCADE"))
    author = db.relationship("User", uselist=False)

    answer_id = db.Column(db.Integer, db.ForeignKey("answers.id"))
    answer = db.relationship("Answer", backref=db.backref(
                            "comments", lazy="dynamic"), uselist=False)

    # question_id = Column(db.Integer, db.ForeignKey("answers.id"))
    # question = db.relationship("Question", backref=db.backref(
    #     "comments", lazy="dynamic"), uselist=False)
class Message(Base, db.Model):
    __tablename__ = 'message'
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    publish_people = db.Column(db.String(128))
    create_date = db.Column(db.DateTime,default=get_current_time)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)



DB_TABLE_MAP = {
    'course':Course,
    'user':User,
    'student':Student,
    'grade':Grade,
}





