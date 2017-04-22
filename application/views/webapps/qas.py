#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from application.db import models
from application.base import BaseManager, render_jinja
from application.utils.query import Pager, success2json,exception2json
import  jieba
render = render_jinja('static/templates/qa', encoding='utf-8')

from flask import Blueprint,session,render_template,url_for,redirect,request

qa = Blueprint('qa', __name__,template_folder="static/templates")

#
# @qa.route("/question/add", methods=["GET", "POST"])
class QaAdd(BaseManager):
    def get(self):
        return render.question_add()
    def post(self):
        params = request.form
        author_id = session.get('username',None)
        dest = []
        title = params.get("title")
        save_title = jieba.cut(title, cut_all=False)
        for t in save_title:
            dest.append(t)
        length = len(dest)
        print dest
        print "lllllllllll",length
        obj = models.Question.query.all()
        if obj:

            for t in obj:
                org = []
                count = 0
                data = jieba.cut(t.name, cut_all=False)
                for d in data:
                    org.append(d)
                for index, value in enumerate(dest):
                    if dest[index] in org:
                        count+=1
                print "cccccccccccc", count
                sum = (float(count)/float(length)) *100
                print "*******", sum
                if sum >= int(50):
                    return exception2json("question exist")
                else:
                    continue

            values = {
                "name":params.get('title'),
                "content":params.get('content'),
                "author_id":author_id,
            }
            print "************* ", values
            models.Question(values).save()
            return success2json("create question success")


# @qa.route("/question/lists", methods=["GET"])
class QaList(BaseManager):

    def get(self):
        current_user = session.get("username", None)
        q_counts = models.Question.query.filter_by(author_id=current_user).count()


        a_counts = models.Answer.query.filter_by(author_id=current_user).count()

        c_counts = models.Comment.query.filter_by(author_id=current_user).count()

        questions = models.Question.query.all()
        print questions, q_counts, a_counts, c_counts
        if questions:
            return render.question_lists(questions=questions,current_user=current_user,
                                         q_counts=q_counts, a_counts=a_counts, c_counts=c_counts)
        else:
            return render.question_lists(current_user=current_user)

class QaDetail(BaseManager):

    def get(self):
        question_id = request.args.get("question_id", None)
        print "222   22",  question_id
        if question_id:
            question = models.Question.query.filter_by(id=question_id).first()

            print "-------------", question.name
            if question:
                return  render.question_detail(question=question)


class AddAnswer(BaseManager):

    def post(self):
        qid = request.form.get("qid", None)
        print  "---------", qid
        author_id = session.get("username")
        question_instance = models.Question.query.filter_by(id=qid).first()
        if  not question_instance:
            return exception2json("qwe is not")
        if request.form.get("rtype") == "1":
            print "oopppppppp"
            count = question_instance.answers_count
            count +=1

            answer = {
                "content":request.form['content'],
                "author_id":author_id,
               "question_id":qid,
            }


            models.Answer(answer).save()
            question_instance.update({"answers_count": count})
        else:
            if request.form.get("rtype") == "2":
                rid = request.form.get("rid", None)
                author_id = session.get("username")
                answer_instance = models.Answer.query.filter_by(id=rid).first()
                if not answer_instance:
                    return exception2json("qwe is not")
                comment = {
                    "content": request.form.get("content"),
                    "answer_id": rid,
                    "author_id": author_id,
                }
                # comment_instance.answers_count += 1
                models.Comment(comment).save()
                count = answer_instance.comments_count
                count += 1
                answer_instance.update({"comments_count": count})
        return success2json("success")


app = Blueprint('qa_app', __name__, template_folder='templates')
app.add_url_rule('/detail', view_func=QaDetail.as_view('qa-detail'))
app.add_url_rule('/lists', view_func=QaList.as_view('qa-list'))
app.add_url_rule('/qs/add', view_func=QaAdd.as_view('qa-add'))
app.add_url_rule('/answer/add', view_func=AddAnswer.as_view('answer-add'))
# app.add_url_rule('/comment/add', view_func=AddCOmment.as_view('comment-add'))

# app.add_url_rule('/lists', view_func=GradeList.as_view('grade_lists'))