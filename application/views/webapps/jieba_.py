#!/usr/bin/env python2
#-*- coding: utf-8 -*-
import jieba
# seg_list = jieba.cut("基于python的大学生信息智能智能管理系统", cut_all=False)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
seg_list = jieba.cut("基于python的大学生信息智能管理系统", cut_all=False)
set_list = jieba.cut("基于python的大学生成绩智能管理系统", cut_all=False)
st = []
ss = []
for i in seg_list:
    # print i
    ss.append(i)
for i in set_list:
    # print i
    st.append(i)
# print st, ss

length = len(ss)
print length
count = 0
for index,value in enumerate(ss):

    # print index,value
    if ss[index] in st:

       count+=1
# per = count / length
sum = (float(count)/float(7))*100
print "%",sum
# print("Default Mode: " + "/".join(seg_list))  # 精确模式


