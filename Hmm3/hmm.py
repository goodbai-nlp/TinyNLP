#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: hmm.py.py
@time: 16-7-9 下午8:50
"""
import math
import os
import re
from dataset import read_dataset
from collections import Counter
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
        self.tagset = set()
        self.wordset = set()
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

        print('HMM model is built.')
        self.postags = [k for k in self.unigram]
        print(self.postags)

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

    def calc(self,res1,res2):
        '''平滑，取对数 平滑的参数是self.ALPHA'''
        return math.log(self.alpha*res1+(1-self.alpha)*res2)

    def emit(self,words, i, tag):
        rob = words[i]
        ss = self.unigram[tag]
        res1 = self.cooc[rob, tag] / float(ss)
        res2 = 1.0 / ss
        prob = self.calc(res1, res2)
        return prob

    def trans(self,tag,tag1):
        ss = float(self.unigram[tag])
        res1 = self.bigram[(tag, tag1)] / ss
        res2 = 1.0 / ss
        prob = self.calc(res1, res2)
        return prob
def viterbi(words,hmm):
    N, T = len(words), len(hmm.postags)

    score = [[-float('inf') for j in range(T)] for i in range(N)]   #存储中间结果
    path = [[-1 for j in range(T)] for i in range(N)]               #存储路径

    for i, word in enumerate(words):
        if i == 0:
            for j, tag in enumerate(hmm.postags):
                score[i][j] = hmm.emit(words, i, tag)+hmm.start[tag]
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
hmm = HMM()
hmm.fit(train_dataset)
sen = u'国家主席江泽民'
sen2 = u'工信处女干事每月经过下属科室都要亲口交代二十四口交换机等技术性器件的安装工作'
for word in __cut(sen,hmm):
    print(word)