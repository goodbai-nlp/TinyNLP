#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
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
sys.path.append('..')
from utils.dataset import read_dict
from collections import Counter

DATA_DIR = os.getcwd()+'/../data/'
TRAIN_FILE = DATA_DIR + 'train/train.txt'
TEST_FILE = DATA_DIR + 'test/dev.txt'
OUT_PUT = os.getcwd() + '/../score/output.txt'


class HMM(object):
    '''隐马模型'''
    
    def __init__(self, alpha=0.5, train_data=None):
        self.alpha = alpha
        self.start = {'B': 0.7689828525554734, 'E': 0.0, 'M': 0.0, 'S': 0.2310171474445266}
        if train_data:
            self.fit(train_data)
    
    def fit(self, train_data):
        self.unigram = Counter()  # 标签出现次数
        self.bigram = Counter()  # 转移
        self.cooc = Counter()  # 发射
        self.idict = {}
        self.big_dict = {}
        self.place_context = {}
        print('build HMM model...')
        self.idict = read_dict()
        self.big_dict = copy.deepcopy(self.idict)
        f = open("tmp.txt", 'wb')
        for item in train_data:
            re_han, re_skip = re.compile(ur"([\u4E00-\u9FA5\s]+)"), re.compile(ur"[^a-zA-Z0-9+#\n]")
            blocks = re_han.findall(item)
            if not blocks:
                continue
            for sentence in blocks:
                # print sentence
                tag = False
                tmp = sentence.strip().split()
                conflict = []
                if (len(tmp)):
                    sourcesen = ''.join(tmp)
                    res = self.raw_seg(sourcesen)
                    # for words in res:
                    index = 0
                    while index < len(res):
                        words = res[index]
                        if len(words) > 1:
                            self.big_dict[words] = 1
                        if len(words) > 1 and (not self.idict.has_key(words)):
                            inputs = ''
                            if index > 0:
                                inputs += res[index - 1]
                            inputs += res[index]
                            if index < len(res) - 1:
                                inputs += res[index + 1]
                            conflict.append(inputs)
                            # print words
                            tag = True
                        index += 1
                    
                    if not tag:
                        continue
                    '''用有歧义的部分训练HMM'''
                    wordtags = self.getTags(tmp)
                    for itm in conflict:
                        id = sourcesen.index(itm)
                        tags = wordtags[id:id + len(itm)]
                        self.unigram.update(tags)
                        for i in range(len(tags) - 1):
                            self.bigram.update([(tags[i], tags[i + 1])])
                        self.cooc.update([(itm[i], tags[i]) for i in range(len(itm))])
                        str = itm + "  " + ''.join(tags) + "\n"
                        f.write(str.encode('utf-8'))
                    '''用有歧义的句子训练HMM
                    tags = wordtags
                    self.unigram.update(tags)
                    for i in range(len(tags) - 1):
                        self.bigram.update([(tags[i], tags[i + 1])])
                    self.cooc.update([(sourcesen[i], tags[i]) for i in range(len(sourcesen))])
                    str = sourcesen + "  "+ ''.join(tags)+ "\n"
                    f.write(str.encode('utf-8'))
                    '''
        print len(self.idict), len(self.big_dict)
        # self.idict = copy.deepcopy(self.big_dict)
        print('HMM model is built.')
        self.postags = [k for k in self.unigram]
    
    def getTags(self, sentence):
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
    
    def raw_seg(self, sentence):
        i, j = 0, 0
        res = []
        tag = False
        while j < len(sentence):
            tag = False
            max_length = self.get_maxlength(j, sentence)
            
            while max_length:
                j = j + max_length
                max_length = self.get_maxlength(j, sentence)
            # yield sentence[i:j + 1]
            res.append(sentence[i:j + 1])
            i = j + 1
            j = i
        return res
    
    def get_maxlength(self, start, sentence):
        tmp = range(min(len(sentence) - start, 7))
        max_length = 0
        for lenh in tmp:
            if lenh and self.idict.has_key(sentence[start:start + lenh + 1]):
                max_length = lenh
        return max_length
    
    def calc(self, res1, res2):
        '''平滑，取对数 平滑的参数是self.ALPHA'''
        return math.log(self.alpha * res1 + (1 - self.alpha) * res2)
    
    def emit(self, words, i, tag):
        rob = words[i]
        try:
            ss = float(self.unigram[tag])
            res1 = self.cooc[rob, tag] / ss
            if (tag == 'S'):
                res1 = res1 * 0.5
        except:
            res1 = 0
        res2 = 1.0 / float(self.unigram[tag])
        
        if i == len(words):
            if tag == 'B' or tag == 'M':
                res1 = 0
        prob = self.calc(res1, res2)
        # prob = math.log((self.cooc[rob,tag]+1) / (ss+ len(words)))
        return prob
    
    def trans(self, tag, tag1):
        '''这里先不用平滑'''
        ss = float(self.unigram[tag])
        res1 = self.bigram[(tag, tag1)] / ss
        res2 = 1.0 / ss
        # prob = self.calc(res1, res2)
        prob = math.log(res1) if self.bigram[(tag, tag1)] else -1e10
        # prob = math.log((self.bigram[tag,tag1]+1)/(ss+len(self.postags)))
        return prob


# def viterbi(words, hmm):
#     N, T = len(words), len(hmm.postags)
#
#     score = [[-float('inf') for j in range(T)] for i in range(N)]  # 存储中间结果
#     path = [[-1 for j in range(T)] for i in range(N)]  # 存储路径
#
#     for i, word in enumerate(words):
#         if i == 0:
#             for j, tag in enumerate(hmm.postags):
#                 tmps = math.log(hmm.start[tag]) if tag not in {'E', 'M'} else -1e20
#                 score[i][j] = hmm.emit(words, i, tag) + tmps
#         else:
#             for j, tag in enumerate(hmm.postags):
#                 # 动态规划计算概率
#                 # Your code here, enumerate all the previous tag
#                 (best, best_t) = max(
#                     [(score[i - 1][y0] + hmm.trans(tag2, tag) + hmm.emit(words, i, tag), y0) for y0, tag2 in
#                      enumerate(hmm.postags) if score[i - 1][y0] > -1e20])
#                 score[i][j] = best
#                 path[i][j] = best_t
#
#     best, best_t = -1e20, -1
#     for j, tag in enumerate(hmm.postags):
#         if best < score[len(words) - 1][j]:
#             best = score[len(words) - 1][j]
#             best_t = j
#
#     result = [best_t]
#     for i in range(len(words) - 1, 0, -1):  # 回溯找出路径
#         result.append(path[i][result[-1]])
#     # convert POStag indexing to POStag str
#     result = [hmm.postags[t] for t in reversed(result)]
#     return result
#
#
# def __cut(sen, hmm, start, lent):
#     pos = viterbi(sen, hmm)
#     pos_list = pos[start:start + lent]
#     sentence = sen[start:start + lent]
#     # print ' '.join(pos_list)
#     res = []
#     begin, next = 0, 0
#     for i, char in enumerate(sentence):
#         pos = pos_list[i]
#         if pos == 'B':
#             begin = i
#         elif pos == 'E':
#             ttmp = ''.join(sentence[begin:i + 1])
#             res.append(ttmp)
#             next = i + 1
#         elif pos == 'S':
#             res.append(char)
#             next = i + 1
#     if next < len(sentence):
#         ttmp = ''.join(sentence[next:])
#         res.append(ttmp)
#     # print ' '.join(res)
#     return res
