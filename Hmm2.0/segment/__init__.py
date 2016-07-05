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
import math
import pickle
MAX_LENGTH = 10
vocab = []


class Graph(object):
    def __init__(self):
        self.seq = []
class Gnode(object):
    def __init__(self,strs):
        self.value = strs
DATA_DIR = os.getcwd()+'/../../data/'
DICT_DIR = DATA_DIR + 'icwb2-data/gold/pku_training_words.utf8'
MODEL_DIR = os.getcwd()+'/../Training/data.dat'

def load_dict(FILE):
    '''生成汉字字典'''
    global vocab
    vocab = []
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
            vocab.append(m.group(0))
            # print ' '.join(idict)
def createGraph(sentence):
    '''生成有向图'''
    gra = Graph()
    for i in range(len(sentence)):
        gra.seq.append({})
    for i in range(len(sentence)):
        for j in range(MAX_LENGTH):
            if i + j + 1 > len(sentence):
                break
            tmp = ''.join(sentence[i:i+j+1])
            if tmp in vocab:
                tmpvalue = Gnode(tmp)
                gra.seq[i+j][tmp] = tmpvalue
    end = Gnode('#')
    gra.seq.append({'#': end})
    return gra
res = ''
allres = []

def dfs(n,graph,sentence,path):
    '''遍历有向图,找出所有路径,存在allres[]中'''
    if n<0:
        # print path
        allres.append(path)
    elif not graph.seq[n]:
        path = sentence[n] + ' ' + path
        dfs(n-1,graph,sentence,path)
    else:
        for key,value in graph.seq[n].items():
            tmppath = key + ' ' + path
            dfs(n-len(key),graph,sentence,tmppath)
def select():
    '''选择最小切分结果'''
    best = []
    best.append(allres[0])
    for item in allres:
        if len(item) < len(best[0]):
            best = []
            best.append(item)
        elif len(item) == len(best[0]):
            best.append(item)
    # print '\n'.join(best)
    return best

def dealstr(sentence):
    res = []
    # print sentence.split(" ")
    for word in sentence.split(' '):
        tmpstr=''
        if not word:
            continue
        if (len(word) == 1):
            tmpstr = 'S'
        else:
            tmpstr = 'B'
            for i in range(1, len(word)):
                if (i + 2 <= len(word)):
                    tmpstr += 'M'
                else:
                    tmpstr += 'E'
        res+=tmpstr
    res2 = ''.join(res)
    # print res2,len(res2)
    ttmp = ''.join(sentence.split(' '))
    # print ttmp,len(ttmp)
    P_state = (-math.log(P_start[states.index(res2[0])]))   #状态概率 P(C)
    for i in range(len(res2)-1):
       P_state += (-math.log(P_trans[states.index(res2[i])][states.index(res2[i+1])]))
    P_mixp = 0                                              #条件概率 P(O|C)
    for i in range(len(res2)):
        P_mixp+= (-math.log(P_mix[states.index(res2[i])][idict.index(ttmp[i])]))
    P_sum = P_state + P_mixp
    print sentence,P_sum
    return (sentence,P_sum)


def cut():
    pass
f = open(MODEL_DIR)
dump_data = pickle.load(f)
P_start = dump_data[0]
P_trans = dump_data[1]
P_mix = dump_data[2]
states = dump_data[3]
idict = dump_data[4]
load_dict(DICT_DIR)
sentence = u'汉字笔顺标准由国家语言文字工作委员会标准化工作委员会制定叫做现代汉语通用字笔顺规范'
sentence2 = u'工信处女干事每月经过下属科室都要亲口交代二十四口交换机等技术性器件的安装工作'

tmp = createGraph(sentence2)
dfs(len(sentence2)-1,tmp,sentence2,'')
best = select()
bestt = ('',1e5)
for sen in best:
    sene,value = dealstr(sen)
    if value<bestt[1]:
        bestt = (sene,value)
print 'best choice:'
print ''.join(bestt[0]),value