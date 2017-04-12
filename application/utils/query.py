#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
from application.db import models
import  math
course = 'course'
from flask import session

def sqlalchemy_obj_to_dict(obj, is_sql_obj=True):
    # TODO
    if hasattr(obj, 'dump'):
        res = obj.dump()
        return res
        # return object2dict(res)
    else:
        dict_result = {}
        fields = []
        relationships = []
        if is_sql_obj:
            dict_result = dict((col.name, _column_json_loads(obj, col))
                for col in class_mapper(obj.__class__).mapped_table.c)

            fields = ( col.name for col in class_mapper(obj.__class__).mapped_table.c )
            relationships = class_mapper(obj.__class__).relationships.keys()
        for d in dir(obj):
            if d.startswith('_') | d.startswith('metadata'):
                continue
            elif d in fields or d in relationships:
                continue
            else:
                key = '%s' %(d)
                val = getattr(obj, d)
                if callable(val):
                    continue
                dict_result[key] = val
        return dict_result

def grid_json(page, total, records, rows, id_attr, cells=[]):
        list_rows = []
        for i in rows:
            id_ = getattr(i, id_attr)
            cell = []
            for j in cells:
                value = getattr(i, j, None)
                if j in ['created_at', 'updated_at', \
                         'launched_at', 'record_at', \
                         'start_at', 'finished_at', 'terminated_at']:
                    value = value.partition('.')[0]
                # if j == 'class_id':
                #    value = models.Class.query.filter_by(id=j)
                if value == 'None':
                    value = ''
                cell.append(value)


                # cell = [str(getattr(i, j, None)) for j in cells]
            list_rows.append({"id": id_, "cell": cell})

        res = {"page": str(page),
               "total": str(total),
               "records": str(records),
               "rows": list_rows}
        print "res res     res" ,res
        return json.dumps(res)

# pager
class Pager:
    # def __init__(self):
    #     pass

    def grid_rows_query(self, table, params, filter_by={}, filter_={}, read_deleted='no', filter_not_equal={}, mode=None):
        #params = {'table': table, 'filter_by': filters, 'mode': 'count'}
        model_object = models.DB_TABLE_MAP.get(table)
        user_id = session.get('username', None)
        print 'qqqqqqqqqqqq', model_object
        records = model_object.query.count()
        if table in ['course', 'grade']:
            records = model_object.query.filter_by(owner=user_id).count()
        # if table in ['grade']:

        print  'records-------------', records
        limit = int(params.get('rows'))  # 每页显示行。
        sord = params.get('sord')  # 升序还是降序
        sidx = params.get('sidx')  # 排序关键字
        page = int(params.get('page')) # 申请的第几页


        offset = limit * (page - 1)
        print "offfff",offset
        total = math.ceil(records / float(limit))
        total = int(total)
        order_by = '%s %s' % (sidx, sord.lower())
        query = model_object.query
        # query = self.get_query(limit, sord, sidx, page, offset, filter_by, filter_)
        if table in ['course','grade']:
            query = model_object.query.filter_by(owner=user_id)


        if filter_by:
            query = model_object.query.filter_by(**filter_by)
        if filter_:
            query = model_object.query.filter(**filter_)
        values = {
            'query':query,
            'order_by':order_by,
            'mode': 'all',
            'limit':limit,
            'offset':offset,
        }
        rows = self.get_rows(**values)

        return (page, total, records, rows)

    def get_rows(self, query, order_by, mode, limit, offset):
        if mode.lower() == 'all':
            if order_by:
                if isinstance(order_by, (tuple, list)):
                    query = query.order_by(*order_by)
                else:
                    query = query.order_by(order_by)
            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)
            dbresult = query.all()
            return dbresult
        # if relationships:
        #     dbresult = getattr(dbresult, str(relationships))


    # def get_query(self,limit, sord, sidx, page, offset, filter_by, filter_):
    #     query = model_object.query()
    #     if filter_by:
    #         query = model_object.query.filter_by(**filter_by)
    #     if filter_:
    #         query = model_object.query.filter(**filter_)
    #     return query


def update_values(values, k, v, is_list=False):
    if v is not None:
        if not v:
            if v == '':
                v = [] if is_list else None
        values[k] = v
    return values


def success2json(msg):
    # print "rrrrrrrrrrr",records
    # records = object2dict(records)

    # if isinstance(records, list):
    #     count = len(records)
    # else:
    #     count = 1

    data = {
        "reply": {
            "is_success": True,
            "error":"",
            "success_msg" : msg,
        },

    }
    return data2json(data), 200

def exception2json(error, status='200'):
    '''return program error to ui,format is json '''
    #if isinstance(error, Exception):
    #    msg = '%s: %s' % (error.__class__.__name__, error)
    msg = '%s' % (error)
    data =  {
        "reply": {
            "is_success": False,
            "error": msg,
        }
    }
    return data2json(data), status

# class DateEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.strftime('%Y-%m-%d %H:%M:%S')
#         elif isinstance(obj, datetime.date):
#             return obj.strftime('%Y-%m-%d')
#         else:
#             return json.JSONEncoder.default(self, obj)
def data2json(obj):
    result = json.dumps(obj)
    # print "***************", result
    # print type(result)
    return result