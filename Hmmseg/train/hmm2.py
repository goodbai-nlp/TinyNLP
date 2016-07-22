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
import copy
from dataset import read_dataset,read_dict
from collections import Counter

DATA_DIR = os.getcwd()+'/data/'
TRAIN_FILE = DATA_DIR + 'train/train.txt'
TEST_FILE = DATA_DIR + 'test/dev.txt'
TEST_FILE2 = DATA_DIR + 'test/pku_test.utf8'
OUT_PUT = os.getcwd() + '/score/output.txt'
OUT_PUT2 = os.getcwd() + '/score/support.txt'

class HMM(object):
    '''隐马模型'''
    def __init__(self,alpha = 0.98,train_data = None):
        self.alpha = alpha
        self.start = {'B':0.7689828525554734, 'E':0.0, 'M':0.0, 'S':0.2310171474445266}
        if train_data:
            self.fit(train_data)

    def fit(self,train_data):
        self.unigram = Counter()       #标签出现次数
        self.bigram =  Counter()        #转移
        self.cooc = Counter()           #发射
        self.wordcount = Counter()      #词计数
        # self.tagset = set()
        # self.wordset = set()
        self.idict = {}
        self.big_dict = {}
        # self.near_dict ={}
        print('build HMM model...')
        self.idict = read_dict()
        self.big_dict = copy.deepcopy(self.idict)
        for item in train_data:
            # paragraph = ''.join()
            re_han, re_skip = re.compile(ur"([\u4E00-\u9FA5\s]+)"), re.compile(ur"[^a-zA-Z0-9+#\n]")
            blocks = re_han.findall(item)
            if not blocks:
                continue
            for sentence in blocks:
                tmp = sentence.strip().split()
                if len(tmp):
                    tags = self.getTags(tmp)
                    print ' '.join(tmp)
                    for sword in tmp:
                        if len(sword)>1:
                            self.big_dict[sword]=1
                    words = list(''.join(tmp))
                    self.unigram.update(tags)
                    # self.tagset |= set(tags)
                    # self.wordset |= set(words)
                    self.wordcount.update(words)
                    for i in range(len(tags)-1):
                        self.bigram.update([(tags[i], tags[i + 1])])
                    self.cooc.update([(words[i], tags[i]) for i in range(len(words))])
        print(len(self.idict),len(self.big_dict))
        # self.get_near()
        print('HMM model is built.')
        self.postags = [k for k in self.unigram]
        # print(self.postags)
    # def get_near(self):
    #     for item in self.idict.keys():
    #         if(item and len(item)>=2):
    #             for i in range(len(item)-1):
    #                 self.near_dict[item[i:i+2]]=1
    #                 # print(item[i:i+2])
    def getTags(self,sentence):
        line_str = []
        for item in sentence:
            # print(item)
            if (len(item) == 1):
                tmpstr = 'S'
            else:
                tmpstr = 'B'
                for i in range(1, len(item)):
                    if (i + 2 <= len(item)):
                        tmpstr += 'M'
                    else:
                        tmpstr += 'E'
            # print(tmpstr)
            line_str += tmpstr
        if len(''.join(sentence)) != len(line_str):
            print ('EEEEEEEEEEEEEEEEEEEEEE')
        return line_str
    def raw_seg(self,sentence):
        i,j=0,0
        res = []
        tag = False
        while j < len(sentence):
            tag = False
            max_length = self.get_maxlength(j,sentence)

            while max_length:
                j = j + max_length
                max_length = self.get_maxlength(j,sentence)
            yield sentence[i:j+1]
            # res.append(sentence[i:j+1])
            i = j+1
            j = i

    def get_maxlength(self,start,sentence):
        tmp = range(min(len(sentence) - start, 6))
        max_length = 0
        for lenh in tmp:
            if lenh and self.idict.has_key(sentence[start:start + lenh + 1]):
                max_length = lenh
        return max_length
    def calc(self,res1,res2):
        '''平滑，取对数 平滑的参数是self.ALPHA'''
        return math.log(self.alpha*res1+(1-self.alpha)*res2)

    def emit(self,words, i, tag):
        rob = words[i]
        try:
            ss = float(self.unigram[tag])
            res1 = self.cooc[rob, tag] / ss
            if(tag=='S'):
                res1 = res1*0.5
        except:
            res1 = 0
        res2 = 1.0 / float(self.unigram[tag])
        # if i<(len(words)-1):
        #     if self.idict.has_key(words[i:i+2]):
        #         res1 = 1.0 if 'B'==tag else 0
        # if i < (len(words) - 2):
        #     if self.idict.has_key(words[i:i + 3]):
        #         res1 = 1.0 if 'B' == tag else 0
        # if i < (len(words) - 3):
        #     if self.idict.has_key(words[i:i+2]) or self.idict.has_key(words[i:i+3]) or self.idict.has_key(words[i:i+4]):
        #         res1 = 1.0 if 'B'==tag else 0
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
        '''这里先不用平滑'''
        ss = float(self.unigram[tag])
        res1 = self.bigram[(tag, tag1)] / ss
        res2 = 1.0 / ss
        # prob = self.calc(res1, res2)
        prob = math.log(res1) if self.bigram[(tag,tag1)] else -1e10
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
    for i in range(len(words) - 1, 0, -1):      #回溯找出路径
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

print (time.strftime('%Y-%m-%d %H:%M:%S'))
train_dataset = read_dataset()

# test_dataset = read_dataset(TEST_FILE)
test_dataset = read_dataset(TEST_FILE2)
hmm = HMM()
hmm.fit(train_dataset)
if __name__ == '__main__':
    separator = ' '
    f = open(OUT_PUT,'wb')
    f2 = open(OUT_PUT2,'wb')
    re_han = re.compile(ur"([\u4E00-\u9FA5]+)")
    re_skip = re.compile(ur"^[a-zA-Z0-9\uff10-\uff19\u2014\uff21-\uff3a\uff41-\uff5a]$")
    print (time.strftime('%Y-%m-%d %H:%M:%S'))
    for line in test_dataset:
        res = ''
        tmpp = ''
        blocks = re_han.split(line.strip())
        for blk in blocks:
            if not blk:
                continue
            if re_han.match(blk):
                # print(blk)
                for ll in hmm.raw_seg(blk):
                    if ll:
                        # print(ll)
                        tmpp=tmpp+ll+'\n'       # for support file
                        if ll in hmm.idict:
                            res += ll
                        else:
                            tmp = __cut(ll, hmm)
                            res += separator.join(tmp)
                        res += separator
            else:
                i=0
                while i<len(blk):
                    ttmp = ''
                    if not re_skip.match(blk[i]):
                        res += blk[i] +separator
                        i+=1
                    else:
                        while (i<len(blk)) and re_skip.match(blk[i]):
                            ttmp+=blk[i]
                            i+=1
                        res += (ttmp+separator)
        if res:
            res+='\n'
            f.write(res.encode('utf-8'))
            f2.write(tmpp.encode('utf-8'))
    print (time.strftime('%Y-%m-%d %H:%M:%S'))
    f.close()