#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session,redirect
from application.base import BaseManager, render_jinja
from application.db import models
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
import smtplib
import email
import os
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

#login_manager = LoginManager()
render = render_jinja('static/templates/user', encoding='utf-8',)


class Mail(object):
    def __init__(self, user, password, **kwargs):
        self.user = user
        self.password = password
        self.myname = None
        self.mail_server = None
        self.mail_port = 0
        self.to_addrs = []
        self.timeout = 5
        self.use_ssl = True
        # self.use_tls = True
        self.attachments = []

        self.__dict__.update(kwargs)

    def sendmail(self, subject, content):
        """send email with smtp.

        :param subject: string|the email's subject
        :param connect: string|the email's connect
        """

        msg = self.pack_msg(subject, content)

        return self._send_mail(msg)

    def _send_mail(self, msg):
        if self.use_ssl:
            server = SMTP_SSL(timeout=self.timeout)
        else:
            server = smtplib.SMTP(timeout=self.timeout)

        try:
            server.connect(host=self.mail_server, port=str(self.mail_port))
            server.login(self.user, self.password)
            res = server.sendmail(self.from_addr, self.to_addrs, msg.as_string())
            return res
        except Exception, e:
            raise e
        finally:
            if getattr(server, 'sock', None):
                server.close()

    def pack_msg(self, subject, content):
        '''

        :param subject: string| mail's subject
        :param content: string| mail's content
        :return: the mail content include attachments file
        '''
        msg = email.MIMEMultipart.MIMEMultipart()
        content_msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg.attach(content_msg)

        msg = self.pack_attach(msg)

        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = ",".join(self.to_addrs)
        return msg

    def pack_attach(self, msg):
        '''

        :param attachments: list| mail's attachments
        :return: the mail content include attachments file
        '''
        if not self.attachments:
            return msg

        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)
        for attachment in self.attachments:
            with open(attachment, 'rb') as data:
                file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
                file_msg.set_payload(data.read())

                email.Encoders.encode_base64(file_msg)
                basename = os.path.basename(attachment)
                file_msg.add_header('Content-Disposition', 'attachment', filename=basename)

                msg.attach(file_msg)
        return msg

    @property
    def from_addr(self):
        username = self.user.split('@')[0]
        myname = self.myname or username
        from_addr = '%s <%s>' % (myname, self.user)
        return from_addr

class UserCreate(BaseManager):

    def get(self):
        return render.user_create()

    def post(self):

        params = request.form
        identity = params.get('identity')

        if identity == 's':
            check_exist = models.User.query.filter_by(id=params.get('student_number')).first()
            if check_exist:
                print '-------------', check_exist.id
                return  exception2json("user already exists")
            values = {
                'id': params.get('student_number'),
                'name': params.get('student_name'),
                'password': params.get('student_password'),
                'mail': params.get('student_mail'),
                'college': params.get('student_college'),
                'subject': params.get('student_subject'),
                'class_': params.get('student_class'),
                'semester': params.get('student_time'),
                'role_id': params.get('student_role')
            }
            print "sssssssssssss", values
            models.User(values).save()
            return  success2json("用户注册成功")
        else:
            check_exist = models.User.query.filter_by(id=params.get('teacher_number')).first()
            if check_exist:
                return exception2json("用户已经存在")
            values = {
                "id":params.get('teacher_number'),
                "password":params.get('teacher_password'),
                "mail":params.get('teacher_mail'),
                "name": params.get('teacher_name'),
                "college": params.get('teacher_college'),
                "subject": params.get('teacher_subject'),
                "role_id": params.get('teacher_role'),
            }
            print "tttttttttt", values
            models.User(values).save()
            return success2json("用户注册成功")


class UserDelete(BaseManager):
    def POST(self):
        pass


class Login:
    def GET(self):
        pass
    def post(self, parmes):
        username = parmes.get('username', '')
        password = parmes.get('password', '')
        identity = parmes.get('identity', '')
        if identity == 'student':
            print "----------", identity
            check_user = models.User.query.filter_by(id=username).first()
            check_password = models.User.query.filter_by(password=password).first()
            if check_user:
                if check_password:
                    return redirect('/home')
            else:
                return exception2json("user not exist")
        elif identity == 'teacher':
            check_user = models.User.query.filter_by(id=username).first()
            check_password = models.User.query.filter_by(password=password).first()
            if check_user:
                if check_password:
                    return redirect('/home')
            else:
                return exception2json("user is not exist")
        else:
            return  render.user_login(tip="erong")


class UserForget(BaseManager):
    def get(self):
        return  render.user_forget()
    def post(self):
        params = request.form
        username = params.get("username")
        usermail = params.get("usermail")
        userobj = models.User.query.filter_by(id=username).first()
        if userobj:
            password = userobj.password
            mail = Mail(user="zhuwei2017@163.com", password="zhuwei123")
            mail.mail_server = "smtp.163.com"
            mail.mail_port = 465
            mail.to_addrs = usermail
            content = u"%s 老师/同学,您的密码为%s,点击链接重新登录 <a href='%s'>登录</a>" %(userobj.name, password, "http:192.168.31.132:27000")
            mail.sendmail("密码找回", content=content)
            return success2json("邮件发送成功")
        else:
            return exception2json("账户不存在")




app = Blueprint('usercreate', __name__, template_folder='templates')
app.add_url_rule('/create', view_func=UserCreate.as_view('user_create'))
# app.add_url_rule('/teacher/create', view_func=UserTeacherCreate.as_view('teacher_create'))
app.add_url_rule('/forget', view_func=UserForget.as_view('user_froget'))
