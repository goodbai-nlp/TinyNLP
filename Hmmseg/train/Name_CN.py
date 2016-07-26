#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: Name_CN.py
@time: 16-7-23 下午10:19
"""
import sys
import time
from math import log
import pickle
import os
from dataset import read_dataset2
from collections import Counter

DATA_DIR = os.getcwd()+'/../data/'
PDict = DATA_DIR + 'train/person.txt'

class CNNAME(object):
    '''人名识别'''
    def __init__(self):
        self.alpha = -29
        self.para1 = 1
        self.para2 = 2
        pass
    def fit(self):
        self.character = Counter()
        self.han_first = Counter()
        self.han_second1 = Counter()
        self.han_second2 = Counter()
        self.han_single = Counter()
        self.distribute = [0.1799,0.7402,0.0575]
        self.Pre_Postdict = {}
        self.contextsum = 0
        dump_data = []
        self.load_dict()
        if not os.path.exists("./dump.dat"):
            train_data = read_dataset2()
            for sentence in train_data:
                index = 0
                sen = sentence.split()
                while index < len(sen):
                    words = sen[index]
                    word1,tag1 = words.rsplit('/', 1)[0],words.rsplit('/',1)[1]
                    # print word,tag
                    if(tag1=='nr'):
                        if(index<len(sen)-1):
                            words = sen[index+1]
                            word2, tag2 = words.rsplit('/', 1)[0], words.rsplit('/', 1)[1]
                            if(tag2=='nr'):
                                # print word1
                                if(len(word1)==2):
                                    self.han_first.update([tuple(word1)])
                                    self.character.update([tuple(word1)])
                                elif(len(word1)==1):
                                    self.han_first.update(word1)
                                    self.character.update(word1)
                                if (len(word2)==1):
                                    self.han_single.update(word2)
                                    self.character.update(word2)
                                if (len(word2)==2):
                                    self.han_second1.update(word2[0])
                                    self.character.update(word2[0])
                                    self.han_second2.update(word2[1])
                                    self.character.update(word2[1])
                                index+=1
                        else:
                            for chr in word1:
                                self.character.update(chr)
                    else:
                        for chr in word1:
                            self.character.update(chr)
                    index+=1
            f1 = open('../data/train/cn_name.txt','rb')
            f2 = open('../data/train/cn_namelist.utf8','wb')
            i = 0
            double=0
            tri=0
            fourth=0
            for line in f1:
                if sys.version < '3.0':
                    if not (type(line) is unicode):
                        try:
                            line = line.decode('utf-8')
                        except:
                            line = line.decode('gbk', 'ignore')
                ll = line.strip().split('#')
                for item in ll:
                    i+=1
                    if len(item)==2:
                        self.han_first.update(item[0])
                        self.han_single.update(item[1])
                        double+=1
                    elif len(item)==3:
                        self.han_first.update(item[0])
                        self.han_second1.update(item[1])
                        self.han_second2.update(item[2])
                        tri +=1
                    elif len(item)==4:
                        self.han_first.update(tuple(item[:2]))
                        self.han_second1.update(item[2])
                        self.han_second2.update(item[3])
                        fourth +=1
                lls = '\n'.join(line.split('#'))
                f2.write(lls.encode('utf-8'))
            print double,tri,fourth,i
            fp = open("./dump.dat",'wb', -1)
            dump_data.append(self.character)
            dump_data.append(self.han_first)
            dump_data.append(self.han_second1)
            dump_data.append(self.han_second2)
            dump_data.append(self.han_single)
            pickle.dump(dump_data,fp,-1)
        
        else:
            fp = open("./dump.dat", 'rb')
            dump_data = pickle.load(fp)
            self.character = dump_data[0]
            self.han_first = dump_data[1]
            self.han_second1 = dump_data[2]
            self.han_second2 = dump_data[3]
            self.han_single = dump_data[4]
            
    def load_dict(self):
        f = open(PDict,'rb')
        for line in f:
            if sys.version < '3.0':
                if not (type(line) is unicode):
                    try:
                        line = line.decode('utf-8')
                    except:
                        line = line.decode('gbk', 'ignore')
            tmp = line.strip().split()
            w,num = tmp[0],tmp[2]
            self.Pre_Postdict[w] = int(num)
        # print self.Pre_Postdict[u'作为']
    def calc(self,res1,res2):
        return log(float(res1)/res2)
    
    def pchr_all(self,chr,num):
        '''统计Wi作姓（或名）用字出现的次数/Wi出现的总次数'''
        para = 7.0
        if num ==0:
            if(len(chr)==1):
                res1 = max(self.han_first[chr],1)
                res2 = para*max(self.character[chr],1)
                return self.calc(res1,res2)
                # return float(res1)/res2
            if(len(chr)==2):
                res1 = max(self.han_first[tuple(chr)],1)
                res2 = para*max(self.character[tuple(chr)],1)
                return self.calc(res1, res2)
        elif num==1:
            res1 = max(self.han_second1[chr],1)
            res2 = para*max(self.character[chr],1)
            return self.calc(res1, res2)
        elif num==2:
            res1 = max(self.han_second2[chr], 1)
            res2 = para*max(self.character[chr], 1)
            return self.calc(res1, res2)
        elif num==3:
            res1 = max(self.han_single[chr], 1)
            res2 = para*max(self.character[chr], 1)
            return self.calc(res1, res2)
    def pchr_name(self,chr,num):
        '''Wi在姓（或名）中使用的次数/ 姓名中的所有姓（或名）使用的总次数'''
        if num ==0:
            res1 = max(self.han_first[chr], 1)
            res2 = sum([value for value in self.han_first.values()])
            return self.calc(res1, res2)
            # return float(res1) / res2
        if num==1:
            res1 = max(self.han_second1[chr], 1)
            res2 = sum([value for value in self.han_second1.values()])
            return self.calc(res1, res2)
        if num==2:
            res1 = max(self.han_second2[chr], 1)
            res2 = sum([value for value in self.han_second2.values()])
            return self.calc(res1, res2)
        if num==3:
            res1 = max(self.han_single[chr], 1)
            res2 = sum([value for value in self.han_single.values()])
            return self.calc(res1, res2)
        
def decode(model,sentence):
    index = 0
    ans = []
    while index<len(sentence):
        if len(sentence[index])==2:
            item = (sentence[index][0],sentence[index][1])
        else:
            item = sentence[index]
        # print type(item)
        if item in model.han_first:
            res = ''
            # BCD型 和 BE型
            if index+2<len(sentence) and len(sentence[index+1])==1 and len(sentence[index+2])==1:
                score1 = log(model.distribute[1])
                if index-1 >=0 and sentence[index-1] in model.Pre_Postdict:
                    if model.Pre_Postdict[sentence[index-1]] >3:
                        score1 += model.para1         # 自定义参数，可调整
                    else:
                        score1 += model.para2         # 自定义参数，可调整
                        
                if index+3 <len(sentence) and sentence[index+3] in model.Pre_Postdict:
                    if model.Pre_Postdict[sentence[index+3]] >3:
                        score1 += model.para1         # 自定义参数，可调整
                    else:
                        score1 += model.para2         # 自定义参数，可调整
                    
                for i in range(3):
                    tmp= model.pchr_all(sentence[index+i],i)+model.pchr_name(sentence[index+i],i)
                    score1+=tmp
                    
                tmp1= model.pchr_all(sentence[index],0)+model.pchr_name(sentence[index],0)
                tmp2= model.pchr_all(sentence[index+1],3)+model.pchr_name(sentence[index+1],3)
                score2 = tmp1+tmp2+log(model.distribute[0])
                if index - 1 >= 0 and sentence[index - 1] in model.Pre_Postdict:
                    if model.Pre_Postdict[sentence[index - 1]] > 3:
                        score2 += model.para1  # 自定义参数，可调整
                    else:
                        score2 += model.para2  # 自定义参数，可调整
                
                if score1/4.0 > score2/2.0 and score1>model.alpha:    #自定义参数，可调整
                    res = sentence[index]+sentence[index+1]+sentence[index+2]
                    ans.append(res)
                elif score1/4.0 < score2/2.0 and score2>model.alpha:
                    res = sentence[index] + sentence[index + 1]
                    ans.append(res)
            elif index+1<len(sentence) and len(sentence[index+1])==1 and len(sentence[index])>1: #诸葛+单字
                tmp1 = model.pchr_all(sentence[index], 0) + model.pchr_name(sentence[index], 0)
                tmp2 = model.pchr_all(sentence[index+1], 3) + model.pchr_name(sentence[index+1], 3)
                score = tmp1 + tmp2+log(model.distribute[0])
                if index - 1 >= 0 and sentence[index - 1] in model.Pre_Postdict:
                    if model.Pre_Postdict[sentence[index - 1]] > 3:
                        score += model.para1  # 自定义参数，可调整
                    else:
                        score += model.para2  # 自定义参数，可调整
                if index + 2 < len(sentence) and sentence[index + 2] in model.Pre_Postdict:
                    if model.Pre_Postdict[sentence[index + 2]] > 3:
                        score += model.para1  # 自定义参数，可调整
                    else:
                        score += model.para2  # 自定义参数，可调整
                if score>= model.alpha:
                    res = sentence[index]+sentence[index+1]
                    ans.append(res)
        index +=1
    # print ' '.join(ans)
    return ' '.join(ans)
def rec_name(sentence):
    cname = CNNAME()
    cname.fit()
    res = decode(cname, sentence)
    return res
