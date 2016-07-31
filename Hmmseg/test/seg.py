#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: seg.py
@time: 16-7-28 上午9:54
"""
import time
import sys
import os
import re
import math
sys.path.append('..')
from model.NameNer import decode,CNNAME
from model.NumNer import NumRec
from model.PlaceNer import PlaceRec
from model.hmm import HMM
from utils.dataset import read_dataset

DATA_DIR = os.getcwd()+'/../data/'
TRAIN_FILE = DATA_DIR + 'train/train.txt'
TEST_FILE1 = 'test.txt'
TEST_FILE2 = 'pku_test.utf8'
OUT_PUT = os.getcwd() + '/../score/output.txt'



def viterbi(words,hmm):
    N, T = len(words), len(hmm.postags)

    score = [[-float('inf') for j in range(T)] for i in range(N)]   #存储中间结果
    path = [[-1 for j in range(T)] for i in range(N)]               #存储路径

    for i, word in enumerate(words):
        if i == 0:
            for j, tag in enumerate(hmm.postags):
                tmps = math.log(hmm.start[tag]) if tag not in {'E','M'} else -1e20
                score[i][j] = hmm.emit(words, i, tag)+tmps
        else:
            for j, tag in enumerate(hmm.postags):
                # 动态规划计算概率
                # Your code here, enumerate all the previous tag
                (best, best_t) = max(
                    [(score[i - 1][y0] + hmm.trans(tag2, tag) + hmm.emit(words, i, tag), y0) for y0, tag2 in
                     enumerate(hmm.postags) if score[i - 1][y0] > -1e20])
                score[i][j] = best
                path[i][j] = best_t

    best, best_t = -1e20, -1
    for j, tag in enumerate(hmm.postags):
        if best < score[len(words) - 1][j]:
            best = score[len(words) - 1][j]
            best_t = j

    result = [best_t]
    for i in range(len(words) - 1, 0, -1):      #回溯找出路径
        result.append(path[i][result[-1]])
    # convert POStag indexing to POStag str
    result = [hmm.postags[t] for t in reversed(result)]
    return result

def __cut(sen,hmm,start,lent):
    pos = viterbi(sen,hmm)
    pos_list = pos[start:start+lent]
    sentence = sen[start:start+lent]
    # print ' '.join(pos_list)
    res = []
    begin, next = 0, 0
    for i, char in enumerate(sentence):
        pos = pos_list[i]
        if pos == 'B':
            begin = i
        elif pos == 'E':
            ttmp = ''.join(sentence[begin:i + 1])
            res.append(ttmp)
            next = i + 1
        elif pos == 'S':
            res.append(char)
            next = i + 1
    if next < len(sentence):
        ttmp = ''.join(sentence[next:])
        res.append(ttmp)
    # print ' '.join(res)
    return res
   
def Name_Replace(namelist,sen):
    for name in namelist.strip().split(' '):
        index = 0
        if len(name)>=3:
            while index<len(sen):
                if index < len(sen)-2 and sen[index]== name[0] and sen[index+1] == name[1] and sen[index+2] == name[2]:
                    tmp = name[1]+name[2]
                    sen = sen[:index+1] + [tmp] + sen[index+3:]
                    index+=1
                index+=1
    return sen
        
if __name__ == '__main__':
    print (time.strftime('%Y-%m-%d %H:%M:%S'))
    train_dataset = read_dataset()
    test_dataset = read_dataset(TEST_FILE1)
    hmm = HMM()
    hmm.fit(train_dataset)
    Pner = PlaceRec()
    Numner = NumRec()
    cname = CNNAME()
    cname.fit()
    separator = ' '
    f = open(OUT_PUT, 'wb')
    re_han = re.compile(ur"([\u4E00-\u9FA5\u25cb]+)")
    re_skip = re.compile(ur"^[\uff0d\-{0,1}a-zA-Z0-9\uff10-\uff19\u2014\uff21-\uff3a\uff41-\uff5a\u2026\u25cb\\.]$")
    print (time.strftime('%Y-%m-%d %H:%M:%S'))
    print 'Start seg...'
    for line in test_dataset:
        res = ''
        tmpp = ''
        blocks = re_han.split(line.strip())
        for blk in blocks:
            if not blk:
                continue
            if re_han.match(blk):
                # print(blk)
                # for ll in hmm.raw_seg(blk):
                index = 0
                wlist = hmm.raw_seg(blk)
                while index < len(wlist):
                    ll = wlist[index]
                    if ll:
                    
                        tmpp = tmpp + ll + '\n'  # for support file
                        if ll in hmm.idict or len(ll) == 1:
                            res += ll
                        else:
                            inputs = ''
                            llen = 0
                            if index - 1 > 0:
                                inputs += wlist[index - 1]
                                llen = len(wlist[index - 1])
                            inputs += wlist[index]
                            if index + 1 < len(wlist):
                                inputs += wlist[index + 1]
                            tmp = __cut(inputs, hmm, llen, len(ll))
                            res += separator.join(tmp)
                        res += separator
                    index += 1
            else:
                i = 0
                while i < len(blk):
                    ttmp = ''
                    if not re_skip.match(blk[i]):
                        res += (blk[i] + separator)
                        i += 1
                    else:
                        while (i < len(blk)) and re_skip.match(blk[i]):
                            ttmp += blk[i]
                            i += 1
                        res += (ttmp + separator)
    
        if res:
            ttmpp = res.strip().split(' ')
            res1 = Numner.NumNer(ttmpp)
            res2 = Pner.Place_Ner(res1)
            namelist = decode(cname, res2)
            res3 = Name_Replace(namelist, res2)
            ans = '\n'.join(res3)
            ans += '\n'
            f.write(ans.encode('utf-8'))
    print 'mission complete'
    print (time.strftime('%Y-%m-%d %H:%M:%S'))
    f.close()