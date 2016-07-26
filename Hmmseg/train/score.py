#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: score.py
@time: 16-7-25 下午11:12
"""
import sys
if __name__ == '__main__':
    f1 = open('nametest.txt')
    f2 = open('namevalue.txt')
    wrong,right = 0,0
    str1 ,str2= '',''
    for l1,l2 in zip(f1,f2):
        if sys.version < '3.0':
            if not (type(l1) is unicode):
                try:
                    l1 = l1.decode('utf-8')
                except:
                    l1 = l1.decode('gbk', 'ignore')
        if sys.version < '3.0':
            if not (type(l2) is unicode):
                try:
                    l2 = l2.decode('utf-8')
                except:
                    l2 = l2.decode('gbk', 'ignore')
        tmp1 = l1.strip().split(' ')
        tmp2 = l2.strip().split(' ')
        for item in tmp2:
            # print item
            if len(item)>=3:
                if item in tmp1:
                    print 'Right:', item
                    right+=1
                else:
                    print 'Wrong:',item
                    wrong+=1
    print 'right:',right,'wrong:',wrong