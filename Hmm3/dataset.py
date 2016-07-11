#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: dataset.py
@time: 16-7-9 下午8:53
"""
from __future__ import print_function
import sys
import os
DATA_DIR = os.getcwd()+'/data/'
TRAIN_FILE = DATA_DIR + 'train.txt'
DATA_DICT = DATA_DIR + 'vocab.txt'
def read_dataset(filename=TRAIN_FILE):
    try:
        # f2 = DATA_DIR + 'HIT_test.txt'
        fp = open(filename, 'r')
        # f = open(f2,'wb')
    except:
        print("Failed to open file.", file=sys.stderr)
        return

    dataset = []
    # i =0
    for line in fp:
        if sys.version < '3.0':
            if not (type(line) is unicode):
                try:
                    line = line.decode('utf-8')
                except:
                    line = line.decode('gbk', 'ignore')
        tokens = line.strip().split()
        tmp = (' '.join([t.rsplit('/', 1)[0] for t in tokens]))
        # if tmp and i< 2000:
        #     i+=1
        #     f.write(tmp.encode('utf-8')+"\n")
        if tmp:
            dataset.append(' '.join([t.rsplit('/', 1)[0] for t in tokens]))
    return dataset

def read_dict(filename=TRAIN_FILE):
    try:
        # f2 = DATA_DIR + 'HIT_test.txt'
        fp = open(filename, 'r')
        # f = open(f2,'wb')
    except:
        print("Failed to open file.", file=sys.stderr)
        return
    idict ={}
    for line in fp:
        if sys.version < '3.0':
            if not (type(line) is unicode):
                try:
                    line = line.decode('utf-8')
                except:
                    line = line.decode('gbk', 'ignore')
        word = line.strip().split(' ')[0]
        idict[word] = 1
    return idict
