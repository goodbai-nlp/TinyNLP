#!/usr/bin/env python
# encoding: utf-8
"""
@version: v 0.1
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: __init__.py
@time: 16-7-4 下午7:24
"""
from hmmlearn import hmm
import numpy as np
import os
import re
MAX_LENGTH = 10
idict = []


class Graph(object):
    def __init__(self):
        self.seq = []
class Gnode(object):
    def __init__(self,strs):
        self.value = strs
DATA_DIR = os.getcwd()+'/../../data/'
DICT_DIR = DATA_DIR + 'icwb2-data/gold/pku_training_words.utf8'

def load_dict(FILE):
    '''生成汉字字典'''
    global idict
    idict = []
    for line in open(FILE, 'rb'):
        if not (type(line) is unicode):
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('gbk', 'ignore')
        line = line.strip()
        if not line or line[0] == '#':
            continue
        re_han = re.compile(ur"([\u4E00-\u9FA5]+)")
        m = re_han.match(line)
        if m:
            idict.append(m.group(0))
            # print ' '.join(idict)
def createGraph(sentence):
    #生成有向图
    gra = Graph()
    for i in range(len(sentence)):
        gra.seq.append({})
    for i in range(len(sentence)):
        for j in range(MAX_LENGTH):
            if i + j + 1 > len(sentence):
                break
            tmp = ''.join(sentence[i:i+j+1])
            if tmp in idict:
                tmpvalue = Gnode(tmp)
                gra.seq[i+j][tmp] = tmpvalue
    end = Gnode('#')
    gra.seq.append({'#': end})
    return gra
res = ''
allres = []
def dfs(n,graph,sentence,path):
    if n<0:
        print path
        allres.append(path)
    elif not graph.seq[n]:
        path = sentence[n] + ' ' + path
        dfs(n-1,graph,sentence,path)
    else:
        for key,value in graph.seq[n].items():
            path = key + ' ' + path
            dfs(n-len(key),graph,sentence,path)
load_dict(DICT_DIR)
sentence = u'今天天气真好'
tmp = createGraph(sentence)
dfs(len(sentence)-1,tmp,sentence,'')
print allres
