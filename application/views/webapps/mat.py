#!/usr/bin/env python2
#-*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import os
dir = "/root/desigine/studentinfomanager/application/static/img"
plt.rcParams['font.sans-serif'] = ['SimHei']
fig, ax = plt.subplots()

bar_x = [1, 1.3, 2, 3, 4]
bar_y = [5,4,22,2,1]
labels = ['<1.0', '1.3-2.0', '2.0-3.0', '3.0-4.0', '4.0>']
plt.xlabel(u'段分布')
plt.ylabel(u'人数')
plt.title(u'智育绩点段分布图')
rect1 = plt.bar(bar_x, bar_y, width=0.1, tick_label=labels ,color='rgb') # or `color=['r', 'g', 'b']`
def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2.0, 1.002*height,
                '%d'%int(height), ha='center', va='bottom')
autolabel(rect1)
ax.set_ybound(0, 40)
plt.tight_layout()
plt.savefig(os.path.join(dir,"t.png"))
plt.show()
# import matplotlib.pyplot as plt

# data = [5, 20, 15, 25, 10]
#
# plt.bar(range(len(data)), data, color='rgb') # or `color=['r', 'g', 'b']`
# plt.show()