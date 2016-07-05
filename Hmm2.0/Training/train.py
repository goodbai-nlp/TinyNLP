#!/usr/bin/env python
# encoding: utf-8
"""
@version: V0.2
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: hmm++.py
@time: 16-7-3 下午7:41
"""
import os
import sys
import re
import time
import pickle
DATA_DIR = os.getcwd()+'/../../data/'
BASE_DICT = DATA_DIR + 'idict.utf8'
TRAIN_FILE = DATA_DIR + 'icwb2-data/training/pku_training.utf8'
idict = []
P_START = [0.7689828525554734, 0.0, 0.0, 0.2310171474445266]
states = ['B', 'E', 'M', 'S']
outputs = []
count_trans = {'B':{'B':0, 'E':0, 'M':0, 'S':0}, 'E':{'B':0, 'E':0, 'M':0, 'S':0}, 'M':{'B':0, 'E':0, 'M':0, 'S':0}, 'S':{'B':0, 'E':0, 'M':0, 'S':0}}
P_transMatrix = {'B':{'B':0, 'E':0, 'M':0, 'S':0}, 'E':{'B':0, 'E':0, 'M':0, 'S':0}, 'M':{'B':0, 'E':0, 'M':0, 'S':0}, 'S':{'B':0, 'E':0, 'M':0, 'S':0}}

count_mixed = {'B':{}, 'E':{}, 'M':{}, 'S':{}}
P_mixedMatrix = {'B':{}, 'E':{}, 'M':{}, 'S':{}}

def enum_dict(filename):
    '''生成汉字字典'''
    global idict
    idict = []
    for line in open(filename,'rb'):
        if not (type(line) is unicode):
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('gbk', 'ignore')
        line = line.strip()
        if not line or line[0] == '#':
            continue
        re_han = re.compile(ur"([\u4E00-\u9FA5])")
        m = re_han.match(line)
        if m:
            idict.append(m.group(0))
    # print ' '.join(idict)
def train_Matrix(filename):
    '''利用统计的方法估计转移矩阵和混淆矩阵'''
    for line in open(filename,'r'):
        if sys.version < '3.0':
            if not (type(line) is unicode):
                try:
                    line= line.decode('utf-8')
                except:
                    line = line.decode('gbk', 'ignore')
        re_han, re_skip = re.compile(ur"([\u4E00-\u9FA5]+)"), re.compile(ur"[^a-zA-Z0-9+#\n]")
        blocks = re_han.findall(line)
        # print ' '.join(blocks)
        if not blocks:
            continue
        line_str = []
        for item in blocks:
            if (len(item) == 1):
                tmpstr = 'S'
            else:
                tmpstr = 'B'
                for i in range(1, len(item)):
                    if (i + 2 <= len(item)):
                        tmpstr += 'M'
                    else:
                        tmpstr += 'E'
            line_str += tmpstr
        if len(''.join(blocks))!=len(line_str):
            print 'EEEEEEEEEEEEEEEEEEEEEE'
            break
        line_item = ''.join(blocks)
        for i in range(len(line_str)-1):
            count_trans[line_str[i]][line_str[i+1]]+=1
        for i in range(len(line_str)-1):
            if line_item[i] not in idict:
                idict.append(line_item[i])
            if line_item[i] not in count_mixed[line_str[i]].keys():
                count_mixed[line_str[i]][line_item[i]] = 1
            else:
                count_mixed[line_str[i]][line_item[i]] += 1

    for key1,value1 in count_trans.items():
        num = sum(value1.values())
        for key2,value2 in value1.items():
            P_transMatrix[key1][key2] = float(value2)/num

    for key1,value1 in count_mixed.items():
        for item in idict:
            if item not in value1:
                count_mixed[key1][item] = 0

    for key1,value1 in count_mixed.items():   #这里采用拉普拉斯平滑来调整
        num = sum(value1.values())
        # print num+len(value1)
        for key2,value2 in value1.items():
            P_mixedMatrix[key1][key2] = float(value2+1)/(num+len(value1))
    # print count_trans
    # print P_transMatrix
    dump_data=[]
    P_trans = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            P_trans[i][j] = P_transMatrix[states[i]][states[j]]
    P_mix = [[0 for i in range(len(idict))]for j in range(4)]
    for i in range(4):
        for j in range(len(idict)):
            P_mix[i][j] = P_mixedMatrix[states[i]][idict[j]]
    f1 = open('./data.dat', 'wb',-1)
    dump_data.append(P_START)
    dump_data.append(P_trans)
    dump_data.append(P_mix)
    dump_data.append(states)
    dump_data.append(idict)
    pickle.dump(dump_data, f1, -1)
print time.strftime('%Y-%m-%d %H:%M:%S')
enum_dict(BASE_DICT)
train_Matrix(TRAIN_FILE)
print time.strftime('%Y-%m-%d %H:%M:%S')