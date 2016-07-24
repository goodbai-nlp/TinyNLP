#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: test.py
@time: 16-7-24 下午3:49
"""
from dataset import read_dataset2

if __name__ == '__main__':
    f = open('nametest.txt','wb')
    train_data = read_dataset2()
    for sentence in train_data:
        if "/nr" in sentence:
            sen = sentence.split()
            tmp = (''.join([t.rsplit('/', 1)[0] for t in sen]))
            f.write((tmp+'\n').encode('utf-8'))
    f.close()