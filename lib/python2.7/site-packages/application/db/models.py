#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import  traceback
from application.apps import db
from sqlalchemy.exc import IntegrityError
from session import get_session

class ORMMethodBase(object):

    def __init__(self, kw_dict={}, *arg, **kw):
        print  'kkkkkkkkkkkkk', kw_dict
        for name, value in kw_dict.iteritems():
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

class BaseA:
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    __table_initialized__ = False
    admission_time = db.Column(db.DateTime)
    semester = db.Column(db.DateTime)



class Root(Base, db.Model):
    __tablename__ = "root"
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))

# class School(Base, db.Model):
#     __tablename__ = "school"
#
#     __table_args__ = (db.UniqueConstraint("name", ),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

#
# class College(Base, db.Model):
#     __tablename__ = "college"
#
#     __table_args__ = (db.UniqueConstraint("name", ),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#     name = db.Column(db.String(255))
#     id = db.Column(db.Integer, primary_key=True)
#
# class Subject(Base, db.Model):
#     __tablename__ = "subject"
#
#     __table_args__ = (db.UniqueConstraint("name", ),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#     name = db.Column(db.String(255))
#     id = db.Column(db.Integer, primary_key=True)
#     college_id = db.Column(db.Integer, db.ForeignKey('college.id'))


class Class(Base, db.Model):
    __tablename__ = "class"
    __table_args__ = (db.UniqueConstraint("name", ),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    students = db.relationship('Student', backref=db.backref('class', order_by=id),
                        primaryjoin='and_(Class.id == Student.class_id,)')

    @property
    def students_num(self):
        return len(self.students)

class Teacher(Base, db.Model):
    __tablename__ = "teacher"
    __table_args__ = (db.UniqueConstraint("teacher_number", ),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    teacher_number = db.Column(db.String(255))
    password = db.Column(db.String(255))
    e_mail = db.Column(db.String(255))
    name = db.Column(db.String(255))
    identity = db.Column(db.String(255))
    telphone = db.Column(db.String(255))
    college = db.Column(db.String(255))
    subject = db.Column(db.String(255))


# class UserStudent(BaseA, Base, db.Model):
#     __tablename__ = "user_student"
#     __table_args__ = (db.UniqueConstraint("student_number", ),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#     id = db.Column(db.Integer, primary_key=True)
#     student_number = db.Column(db.String(255))
#     e_mail = db.Column(db.String(255))
#     password = db.Column(db.String(255))



class Student(Base, BaseA, db.Model):
    __tablename__ = "student"
    __table_args__ = (db.UniqueConstraint("student_number", ),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(255))
    # school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    # college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=True)
    # subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=True)
    xuejichange_id = db.Column(db.Integer, db.ForeignKey('xuejichange.id'), nullable=True)
    # s_password = db.Column(db.String(255))
    # s_number = db.Column(db.String(255))
    # s_e_mail = db.Column(db.String(255))
    telphone = db.Column(db.String(255))
    political = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    job = db.Column(db.String(255))
    # s_id = db.Column(db.String(255))
    student_number = db.Column(db.String(255))
    e_mail = db.Column(db.String(255))
    password = db.Column(db.String(255))
    college = db.Column(db.String(255))
    subject = db.Column(db.String(255))


class XueJiChange(Base, BaseA, db.Model):
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

class Course(Base, BaseA, db.Model):
    __tablename__ = "course"
    __table_args__ = (db.UniqueConstraint("c_name", ),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(255))
    c_score = db.Column(db.Integer)
    c_number = db.Column(db.String(255))

class Grade(Base, BaseA, db.Model):
    __tablename__ = "grade"
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    college = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    student_class = db.Column(db.String(255))
    student_name = db.Column(db.String(255))
    studnet_number = db.Column(db.String(255))
    current_date = db.Column(db.Integer)
    courses = db.relationship('GradeCourse', backref=db.backref('grade', order_by=id),
                               primaryjoin='and_(Grade.id == GradeCourse.grade_id,)')


class GradeCourse(db.Model):
    __tablename__ = "grade_course"
    __table_args__ = (db.UniqueConstraint("c_name", ),
                      {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    student_c_name = db.Column(db.String(255))
    student_c_score = db.Column(db.Integer)
    student_c_number = db.Column(db.String(255))
    student_c_result = db.Column(db.Integer)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=True)


class LeaveApply(Base, db.Model):
    __tablename__ = "leaveapply"
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    status = db.Column(db.String(255))

# class Grade(Base, db.Model):
#     __tablename__ = "grade"
#     __table_args__ =  (db.UniqueConstraint("name", ),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})

# class AuthRole(Base, db.Model):
#     __tablename__ = "auth_role"
#
#     __table_args__ = (db.UniqueConstraint("name"),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     students = db.relationship("Student", backref=db.backref('auth_roles', order_by=id),
#                                primaryjoin='and_(Student.auth_role_id == AuthRole.id,)')
#     teachers = db.relationship("Teacher", backref=db.backref('teacher_roles', order_by=id),
#                                primaryjoin='and_(Teacher.auth_role_id == AuthRole.id,)')
#
# teacher_and_student = db.Table("teacher_and_student",
#        db.Column("teacher_id", db.Integer, db.ForeignKey("student.id")),
#        db.Column("student_id", db.Integer, db.ForeignKey("teacher.id")),
#                                )
#
# class Teacher(Base, db.Model):
#     __tablename__ = "teacher"
#
#     __table_args__ = (db.UniqueConstraint('name',),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#
#     id = db.Column(db.Integer, primary_key=True)
#
#     normal_person = db.Column(db.Integer)
#     current_person = db.Column(db.Integer)
#     left_person = db.Column(db.Integer)
#     over_person = db.Column(db.Integer)
#     identity_role_id = db.Column(db.Integer, db.ForeignKey('identity_role.id'), nullable=True)
#     auth_role_id = db.Column(db.Integer, db.ForeignKey('auth_role.id'), nullable=True)
#
#     name = db.Column(db.String(255))
#     description = db.Column(db.String(255))
#     students = db.relationship("Student", backref=db.backref("teachers", lazy='dynamic'),
#                                secondary=teacher_and_student
#                                )
#     @property
#     def normal(self):
#         return  "%s" % self.normal_person
#     @property
#     def left(self):
#         return "%s" % self.left_person
#     @property
#     def over(self):
#         return "%s" % self.over_person
#     @property
#     def current(self):
#         return "%s" % self.current_person
#
# class Student(Base, db.Model):
#     __tablename__ = "student"
#
#     __table_args__ = (db.UniqueConstraint("name",),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     description = db.Column(db.String(255))
#     auth_role_id = db.Column(db.Integer, db.ForeignKey('auth_role.id'), nullable=True)
#
# class IdentityRole(Base, db.Model):
#     __tablename__ = "identity_role"
#
#     __table_args__ = (db.UniqueConstraint("name",),
#                       {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     number = db.Column(db.Integer)

    #teachers = db.relationship("Teacher", backref=db.backref('teacher_roles', order_by=id),
                             # primaryjoin='and_(Teacher.identity_role_id == IdentityRole.id,'
                             #             'IdentityRole.deleted == False)')
#
#

DB_TABLE_MAP = {
    'course':Course,
    'student':Student,
    'class':Class,
}





