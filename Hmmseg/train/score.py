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

if __name__ == '__main__':
    f1 = open('nametest.txt')
    f2 = open('namevalue.txt')
    wrong,right = 0,0
    for l1,l2 in zip(f1,f2):
        tmp1 = str(l1.strip).split(' ')
        tmp2 = str(l2.strip).split(' ')
        print l1.strip(),'----------',l2.strip()
        for item in tmp2:
            if item in tmp1:
                right+=1
            else:
                wrong+=1
    print 'right:',right,'wrong:',wrong