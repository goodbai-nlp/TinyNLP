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

def read_dataset(filename=TRAIN_FILE):
    try:
        fp = open(filename, 'r')
    except:
        print("Failed to open file.", file=sys.stderr)
        return

    dataset = []
    for line in fp:
        if sys.version < '3.0':
            if not (type(line) is unicode):
                try:
                    line = line.decode('utf-8')
                except:
                    line = line.decode('gbk', 'ignore')
        tokens = line.strip().split()
        dataset.append(' '.join([t.rsplit('/', 1)[0] for t in tokens]))
    return dataset
