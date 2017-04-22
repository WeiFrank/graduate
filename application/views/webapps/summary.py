#!/usr/bin/env python2
#-*- coding: utf-8 -*-
from flask import Blueprint, request,session
from application.base import BaseManager, render_jinja
from search import GradeList,Unpass,Honoer
from calculation import  Clculation

import json
import  os
import numpy as np
import matplotlib.pyplot as plt
dir = "/root/desigine/studentinfomanager/local/lib/python2.7/site-packages/application/static/img/"
from application.db import  models
from application.utils import exception
from application.utils.query import Pager, success2json,exception2json,\
    grid_json,data2json,update_values
render = render_jinja('static/templates/summary', encoding='utf-8',)
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname = "/usr/share/fonts/truetype/simhei.ttf", size=14)


class GuaKe:
    def __init__(self,a,b,c,d,e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def deal(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots()

        bar_x = [1, 1.3, 2, 3, 4]
        bar_y = [self.a, self.b, self.c, self.d, self.e]
        labels = ['<1.3', '1.3-2.0', '2.0-3.0', '3.0-4.0', '4.0>']
        plt.xlabel(u"智育绩点段分布", fontproperties=font)
        plt.ylabel(u'人数', fontproperties=font)
        plt.title(u'班级智育绩点段分布图', fontproperties=font)
        rect1 = plt.bar(bar_x, bar_y, width=0.1, tick_label=labels, color='rgb')  # or `color=['r', 'g', 'b']`

        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2.0, 1.002 * height,
                        '%d' % int(height), ha='center', va='bottom')

        autolabel(rect1)
        ax.set_ybound(0, 30)
        plt.tight_layout()
        plt.savefig(os.path.join(dir, "unpass.png"))
        # plt.show()
class Hon:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d


    def deal(self):
        fig, ax = plt.subplots()
        bar_x = [0.5, 1, 1.5, 2]
        bar_y = [self.a, self.b, self.c, self.d]
        labels = [u'国家级', u'省级', u'市级', u'校级']
        plt.xlabel(u'获奖级别', fontproperties=font)
        plt.ylabel(u'人数', fontproperties=font)
        plt.title(u'班级获奖统计', fontproperties=font)
        rect1 = plt.bar(bar_x, bar_y, width=0.1, tick_label=labels, color='rgb')  # or `color=['r', 'g', 'b']`
        plt.xticks(bar_x, labels, fontproperties=font)
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2.0, 1.002 * height,
                        '%d' % int(height), ha='center', va='bottom')

        autolabel(rect1)
        ax.set_ybound(0, 25)
        plt.tight_layout()
        plt.savefig(os.path.join(dir, "honoer.png"))
        # plt.show()
class SummaryAll(BaseManager):
    def get(self):
        # print "------------------------"
        return render.summary_all()
    def post(self):

        params = request.form
        class_ = params.get("class_")
        semester = params.get("semester")
        # flag = params.get("flag")
        print class_, semester
        #
        # obj_un = Unpass(class_, semester)
        # result_un = obj_un.get_unpass()
        # if result_un:
        #     print result_un


        obj_cal = Clculation(class_, semester)
        result_cal = obj_cal.deal_cal()

        if result_cal:
            ll = []
            low = []
            middle = []
            high = []
            hh = []
            for r in result_cal:
                if float(r['point']) < float(1.3):
                    ll.append(r)
                elif float(r['point']) >= float(1.3) and float(r['point']) < int(2):
                    low.append(r)
                elif float(r['point']) >= int(2) and  float(r['point']) < int(3):
                    middle.append(r)
                elif float(r['point']) >= int(3) and float(r['point']) < int(4):
                    high.append(r)
                else:
                    if float(r['point']) >= int(4):
                        hh.append(r)

            a = len(ll)
            b = len(low)
            c = len(middle)
            d = len(high)
            e = len(hh)
            if os.path.exists(os.path.join(dir, "unpass.png")):
                os.remove(os.path.join(dir, "unpass.png"))
            guake = GuaKe(a,b,c,d,e)
            guake.deal()


        obj_hon = Honoer(class_)
        print "----------------------", obj_hon
        cs, ps, sh, ss = obj_hon.get_honoer()

        a = len(cs)
        b = len(ps)
        c = len(sh)
        d = len(ss)
        if os.path.exists(os.path.join(dir, "honoer.png")):
            os.remove(os.path.join(dir, "honoer.png"))
        h = Hon(a, b, c, d)
        h.deal()

        obj_unpass = Unpass(class_,semester)
        result_unpass = obj_unpass.get_unpass()
        if result_unpass:
            course = []
            print "9999999999999",result_unpass
            for k,v in result_unpass.iteritems():
                if k == 'course_name':
                    course.append(k)


        #
#
        return render.summary_all()


app = Blueprint('summary_app', __name__, template_folder='templates')
app.add_url_rule('/show', view_func=SummaryAll.as_view('summary_lists'))