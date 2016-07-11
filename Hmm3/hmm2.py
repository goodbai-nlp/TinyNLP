#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: hmm2.py
@time: 16-7-11 下午9:03
"""
import math
import os
import re
import sys
import time
from dataset import read_dataset,read_dict
from collections import Counter

DATA_DIR = os.getcwd()+'/data/'
TRAIN_FILE = DATA_DIR + 'train.txt'
TEST_FILE = DATA_DIR + 'hit_test.txt'
OUT_PUT = os.getcwd() + '/score/output.txt'
DATA_DICT = DATA_DIR + 'vocab.txt'
class HMM(object):
    '''隐马模型'''
    def __init__(self,alpha = 0.90,train_data = None):
        self.alpha = alpha
        self.start = {'B':0.7689828525554734, 'E':0.0, 'M':0.0, 'S':0.2310171474445266}
        if train_data:
            self.fit(train_data)

    def fit(self,train_data,train_dict):
        self.unigram = Counter()       #标签出现次数
        self.bigram =  Counter()        #转移
        self.cooc = Counter()           #发射
        self.wordcount = Counter()      #词计数
        self.tagset = set()
        self.wordset = set()
        self.idict = {}
        self.near_dict ={}
        print('build HMM model...')
        for item in train_data:
            re_han, re_skip = re.compile(ur"([\u4E00-\u9FA5]+)"), re.compile(ur"[^a-zA-Z0-9+#\n]")
            blocks = re_han.findall(item)
            if not blocks:
                continue
            tags = self.getTags(blocks)
            words = list(''.join(blocks))
            self.unigram.update(tags)
            self.tagset |= set(tags)
            self.wordset |= set(words)
            self.wordcount.update(words)

            for i in range(len(tags)-1):
                self.bigram.update([(tags[i], tags[i + 1])])
            self.cooc.update([(words[i], tags[i]) for i in range(len(words))])

        self.idict = read_dict(DATA_DICT)
        self.get_near()
        print('HMM model is built.')
        self.postags = [k for k in self.unigram]
        # print(self.postags)
    def get_near(self):
        for item in self.idict.keys():
            if(item and len(item)>=2):
                for i in range(len(item)-1):
                    self.near_dict[item[i:i+2]]=1
                    # print(item[i:i+2])
    def getTags(self,sentence):
        line_str = []
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
            line_str += tmpstr
        if len(''.join(sentence)) != len(line_str):
            print ('EEEEEEEEEEEEEEEEEEEEEE')
        return line_str
    def raw_seg(self,sentence):
        i,j=0,0
        while j < len(sentence) - 1:
            if not self.near_dict.has_key(sentence[j:j + 2]):
                yield sentence[i:j + 1]
                i = j + 1
            j += 1
        yield sentence[i:j + 1]
    def calc(self,res1,res2):
        '''平滑，取对数 平滑的参数是self.ALPHA'''
        return math.log(self.alpha*res1+(1-self.alpha)*res2)

    def emit(self,words, i, tag):
        rob = words[i]
        try:
            ss = float(self.unigram[tag])
            res1 = self.cooc[rob, tag] / ss
        except:
            res1 = 0
        res2 = 1.0 / float(self.unigram[tag])
        if i<(len(words)-1):
            if self.idict.has_key(words[i:i+2]):
                res1 = 1.0 if 'B'==tag else 0
        if i < (len(words) - 2):
            if self.idict.has_key(words[i:i + 3]):
                res1 = 1.0 if 'B' == tag else 0
        if i < (len(words) - 3):
            if self.idict.has_key(words[i:i+2]) or self.idict.has_key(words[i:i+3]) or self.idict.has_key(words[i:i+4]):
                res1 = 1.0 if 'B'==tag else 0
        # if i>3 and i<len(words)-1:
        #     if self.idict.has_key(words[i-1:i+1]) or self.idict.has_key(words[i-2:i+1]) or self.idict.has_key(words[i-3:i+1]):
        #         res1 = 1.0 if 'E' == tag else 0
        # if i < (len(words) - 2) and i > 1:
        #     if self.idict.has_key(words[i-1:i+2]) or self.idict.has_key(words[i-2:i+2]):
        #         res1 = 1.0 if 'M' == tag else 0
        # if i and i<(len(words)-3):
        #     if self.idict.has_key(words[i-1:i+3]):
        #         res1 = 1.0 if 'M' == tag else 0
        if i == len(words):
            if tag == 'B' or tag == 'M':
                res1 = 0
        prob = self.calc(res1, res2)

        # prob = math.log((self.cooc[rob,tag]+1) / (ss+ len(words)))
        return prob

    def trans(self,tag,tag1):
        ss = float(self.unigram[tag])
        res1 = self.bigram[(tag, tag1)] / ss
        res2 = 1.0 / ss
        prob = self.calc(res1, res2)
        # prob = math.log((self.bigram[tag,tag1]+1)/(ss+len(self.postags)))
        return prob

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
    for i in range(len(words) - 1, 0, -1):
        # Your code here, back trace to recover the full viterbi decode path
        result.append(path[i][result[-1]])
    # convert POStag indexing to POStag str
    result = [hmm.postags[t] for t in reversed(result)]
    return result

def __cut(sentence,hmm):
    pos_list = viterbi(sentence,hmm)
    begin, next = 0, 0
    for i, char in enumerate(sentence):
        pos = pos_list[i]
        if pos == 'B':
            begin = i
        elif pos == 'E':
            yield sentence[begin:i + 1]
            next = i + 1
        elif pos == 'S':
            yield char
            next = i + 1
    if next < len(sentence):
        yield sentence[next:]

train_dataset = read_dataset()
train_dict = read_dataset(DATA_DICT)
test_dataset = read_dataset(TEST_FILE)
hmm = HMM()
hmm.fit(train_dataset,train_dict)
if __name__ == '__main__':
    f = open(OUT_PUT,'wb')
    re_han = re.compile(ur"([\u4E00-\u9FA5]+)")
    re_skip = re.compile(ur"^[a-zA-Z0-9\uff10-\uff19\u2014\uff21-\uff3a\uff41-\uff5a]$")
    # re_skip2 = re.compile(ur"")
    print (time.strftime('%Y-%m-%d %H:%M:%S'))
    # test_dataset = [u'回到ＣＤＭＡ覆盖地区再还原']
    for line in test_dataset:
        res = ''
        blocks = re_han.split(line.strip())
        for blk in blocks:
            if not blk:
                continue
            if re_han.match(blk):
                for ll in hmm.raw_seg(blk):
                    if ll:
                        # print(ll)
                        if ll in hmm.idict:
                            res += ll
                        else:
                            tmp = __cut(ll, hmm)
                            res += ' '.join(tmp)
                        res += ' '
            else:
                i=0
                while i<len(blk):
                    ttmp = ''
                    if not re_skip.match(blk[i]):
                        res += blk[i] +' '
                        i+=1
                    else:
                        while (i<len(blk)) and re_skip.match(blk[i]):
                            ttmp+=blk[i]
                            i+=1
                        res += (ttmp+' ')
        if res:
            res+='\n'
            f.write(res.encode('utf-8'))
    print (time.strftime('%Y-%m-%d %H:%M:%S'))
    # print(len(hmm.idict))
    # print(u'还原' in hmm.near_dict)
    # print(u'目前' in hmm.idict.keys())
    # for item in hmm.idict.keys():
    #     print(item)
    # f.close()