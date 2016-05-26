#!/usr/bin/env python
# encoding: utf-8
"""
@version: 0.1
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: PreDeal.py
@time: 16-5-23 下午10:03
"""
import sys
import re
import copy

SUPERSTR = ''
ARTICLE = ''
PROB_TMP = {'B': 0.0, 'E': 0.0, 'M': 0.0, 'S': 0.0}
PROB_START = copy.deepcopy(PROB_TMP)
TEXT = ''

def deal(sentence):
    global SUPERSTR
    global ARTICLE
    global PROB_TMP
    global TEXT
    if sys.version < '3.0':
        if not (type(sentence) is unicode):
            try:
                sentence = sentence.decode('utf-8')
            except:
                sentence = sentence.decode('gbk', 'ignore')
    re_han, re_skip = re.compile(ur"([\u4E00-\u9FA5]+)"), re.compile(ur"[^a-zA-Z0-9+#\n]")
    # blocks = re_han.split(sentence)
    blocks = re_han.findall(sentence)
    ARTICLE += ''.join(blocks)
    TEXT += ' '.join(blocks)
    TEXT+='\n'
    tmp = analyze1(blocks)
    SUPERSTR += tmp
    if (tmp):
        if tmp[0] == 'B':
            PROB_TMP['B'] += 1
        elif tmp[0] == 'S':
            PROB_TMP['S'] += 1


def analyze1(sentence):
    res = ''
    for item in sentence:
        if (len(item) == 1):
            tmpstr = 'S'
        else:
            tmpstr = 'B'
            for i in range(1, len(item)):
                if (i + 2 <= len(item)):
                    tmpstr += 'M'
                else:
                    tmpstr += 'E'
        res += tmpstr
    return res


def GetMatrix(sstr):
    Matrix = {'B': {'E': 0, 'M': 0},
              'E': {'B': 0, 'S': 0},
              'M': {'E': 0, 'M': 0},
              'S': {'B': 0, 'S': 0}}
    for i in range(len(sstr) - 1):
        A = sstr[i];B = sstr[i + 1]
        if A == 'B' and B == 'E':
            Matrix['B']['E'] += 1
            continue
        if A == 'B' and B == 'M':
            Matrix['B']['M'] += 1
            continue
        if A == 'E' and B == 'B':
            Matrix['E']['B'] += 1
            continue
        if A == 'E' and B == 'S':
            Matrix['E']['S'] += 1
            continue
        if A == 'M' and B == 'E':
            Matrix['M']['E'] += 1
            continue
        if A == 'M' and B == 'M':
            Matrix['M']['M'] += 1
            continue
        if A == 'S' and B == 'B':
            Matrix['S']['B'] += 1
            continue
        if A == 'S' and B == 'S':
            Matrix['S']['S'] += 1
            continue
    Matrix2 = copy.deepcopy(Matrix)
    Matrix2['B']['E'] = float(Matrix['B']['E']) / (Matrix['B']['E'] + Matrix['B']['M'])
    Matrix2['B']['M'] = float(Matrix['B']['M']) / (Matrix['B']['E'] + Matrix['B']['M'])
    Matrix2['E']['B'] = float(Matrix['E']['B']) / (Matrix['E']['B'] + Matrix['E']['S'])
    Matrix2['E']['S'] = float(Matrix['E']['S']) / (Matrix['E']['B'] + Matrix['E']['S'])
    Matrix2['M']['E'] = float(Matrix['M']['E']) / (Matrix['M']['E'] + Matrix['M']['M'])
    Matrix2['M']['M'] = float(Matrix['M']['M']) / (Matrix['M']['E'] + Matrix['M']['M'])
    Matrix2['S']['B'] = float(Matrix['S']['B']) / (Matrix['S']['B'] + Matrix['S']['S'])
    Matrix2['S']['S'] = float(Matrix['S']['S']) / (Matrix['S']['B'] + Matrix['S']['S'])
    return Matrix2


def analyze2():
    dicts = {}
    PROB_EMIT = {}
    for i in range(len(SUPERSTR)):
        tmp = (SUPERSTR[i], ARTICLE[i])
        if tmp in dicts:
            dicts[tmp] += 1
        else:
            dicts[tmp] = 0
    for key,value in dicts.items():
        if key[0] in PROB_EMIT:
            if not (key[1] in PROB_EMIT[key[0]]):
                PROB_EMIT[key[0]][key[1]] = float(value)/SUPERSTR.count(key[0])
        else:
            PROB_EMIT[key[0]] = {}
            PROB_EMIT[key[0]][key[1]] = float(value)/SUPERSTR.count(key[0])
    return PROB_EMIT

if __name__ == "__main__":
    for line in open('seg.txt', 'rb'):
        deal(line)
    f0 = open('target.txt','wb')
    f0.writelines(TEXT.encode('utf-8'))
    A = GetMatrix(SUPERSTR)
    PROB_START['S'] = PROB_TMP['S'] / (PROB_TMP['S'] + PROB_TMP['B'])
    PROB_START['B'] = PROB_TMP['B'] / (PROB_TMP['S'] + PROB_TMP['B'])
    B= analyze2()
    f1 = open('prob_start.py','wb')
    f2 = open('prob_trans.py','wb')
    f3 = open('prob_emit.py','wb')
    f1.write(str(PROB_START))
    f2.write(str(A))
    f3.write(str(B))


