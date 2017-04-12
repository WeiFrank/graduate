#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from application.db import models
from application.base import BaseManager, render_jinja
from application.utils.query import Pager, success2json,exception2json

render = render_jinja('static/templates/qa', encoding='utf-8')

from flask import Blueprint,session,render_template,url_for,redirect,request

qa = Blueprint('qa', __name__,template_folder="static/templates")


@qa.route("/question/add", methods=["GET", "POST"])
def add_question():
    if request.method == 'GET':

        return render_template("qa/question_add.html")
    if request.method == 'POST':
        params = request.form
        author_id = session.get('username',None)
        values = {
            "name":params.get('title'),
            "content":params.get('content'),
            "author_id":author_id,
        }
        print "************* ", values
        models.Question(values).save()
        return success2json("create question success")
    # else:
    #     print "-----------", question_id
    #     return  None

@qa.route("/question/lists", methods=["GET"])
def questions_list():
    current_user = session.get("username", None)
    q_counts = models.Question.query.filter_by(author_id=current_user).count()


    a_counts = models.Answer.query.filter_by(author_id=current_user).count()

    c_counts = models.Comment.query.filter_by(author_id=current_user).count()

    questions = models.Question.query.all()
    if questions:
        return render_template("qa/question_lists.html", questions=questions,current_user=current_user,
                                     q_counts=q_counts, a_counts=a_counts, c_counts=c_counts)
    else:
        return render_template("qa/question_lists.html",current_user=current_user)
    # return  render_template("question_lists.html", current_user=current_user)
    # else:
    #     return exception2json("please create question")
@qa.route("/question/detail/", methods=["GET", "POST"])
def question_detail():
    question_id = request.args.get("question_id", None)
    print "222   22",  question_id
    if question_id:
        question = models.Question.query.filter_by(id=question_id).first()

        print "-------------", question.name
        if question:
            return  render_template("qa/question_detail.html", question=question)

@qa.route("/add/answer", methods=["GET","POST"])
def add_answer():
    qid = request.form.get("qid", None)
    author_id = session.get("username")
    question_instance = models.Question.query.filter_by(id=qid).first()
    count = question_instance.answers_count
    count +=1

    if  not question_instance:
        return exception2json("qwe is not")
    else:
        answer = {
            "content":request.form['content'],
            "author_id":author_id,
           "question_id":qid,
        }


        models.Answer(answer).save()
        question_instance.update({"answers_count": count})
    return success2json("pp")

@qa.route("/add/comment", methods=["GET","POST"])
def add_comment():
    aid = request.form.get("aid", None)
    author_id = session.get("username")
    answer_instance = models.Answer.query.filter_by(id=aid).first()
    count = answer_instance.comments_count
    count += 1
    if  not answer_instance:
        return exception2json("qwe is not")
    else:
        comment = {
            "content": request.form.get("content"),
            "answer_id":aid,
            "author_id":author_id,
        }
        # comment_instance.answers_count += 1
        models.Comment(comment).save()
        answer_instance.update({"comments_count":count})
    return  success2json("oj")
