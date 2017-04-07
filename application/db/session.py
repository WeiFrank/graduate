#!/usr/bin/env python2
# -*- coding: utf-8 -*-

db_global = None

def init_db_session(db):
    global db_global

    if db_global is None:
        db_global = db
    return db


def get_session():
    return db_global.session
