#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from xlrd import open_workbook
files = '/root/desigine/studentinfomanager/application/static/upload/131_2016-2017秋.xls'
from collections import OrderedDict
data = open_workbook(files)
print data
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols
print  nrows
print  ncols
# print table.row_values(0)
# print table.col_values(1)

# row[0] [1]
course_number = table.row_values(5)[11]
# course_name = table.col_values(9)
# print  course_name
# print course_number
# for row in range(4,nrows):
#     number += table.row_values(row)[1]+','
#     name += table.row_values(row)[4] +','
# print  course_number
# course = {"score":None, "type":None,"number":None}
# people = {
#     "name":{},
#     "number":{}
# }


class DealTable(object):
    def __init__(self, p_col_start=None, p_col_end=None, p_row_start=None, p_row_end=None):

        self.p_col_start = p_col_start
        self.p_col_end = p_col_end
        self.p_row_start = p_row_start
        self.p_row_end = p_row_end
        count = 0
    def deal_score(self):
        # print course
        course = {}
        # info = {}
        count = 0
        for row in range(self.p_row_start, self.p_row_end):

            for col in range(self.p_col_start, self.p_col_end):

                # if not table.row_values(row)[col]:
                #     continue
                # else:
                print  "*********",table.col_values(col)[0]

                subd = course[table.col_values(col)[0]] = {}

                course[table.col_values(col)[0]]['grade'] = table.row_values(row)[col]
                subd['number'] = table.row_values(self.p_row_start - 4)[col]
                subd['type'] = table.row_values(self.p_row_start - 3)[col]
                subd['score'] = table.row_values(self.p_row_start - 2)[col]

                print "---------", table.row_values(row)[col], table.row_values(self.p_row_start - 4)[col]
                # info['number'] = table.row_values(row)[self.p_col_start-4]
                # info['name'] = table.row_values(row)[self.p_col_start-1]
                # course.update(info)

                # print table.row_values(row)[self.p_col_start-4],table.row_values(row)[self.p_col_start-1]
            print course


t = DealTable(5, 12, 5, 7)
t.deal_score()
values = {
    "college":"tonxin",
    "subject":"diani",
    "class_":"diani131",
    "number":"2013131018",
    "name":"zhuwei",
    "semester":"2013-2014",
    "detail":{"course_a":{"score":2,"grade":99,"type":"bixiu", "number":2342},
              "course_b":{"score":3,"grade":88, "type":"fuxiu","number":23534},
             }
}
