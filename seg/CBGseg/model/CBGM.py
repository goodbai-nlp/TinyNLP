# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from math import log
import sys
sys.path.append("..")
from utils import frequency
import copy

class CBGM(object):
    
    '''CharacterBasedGenerativeModel,in paper y09_2047'''
    
    def __init__(self):
        self.l1 = 0.0;self.l2 = 0.0;self.l3 = 0.0
        self.status = ('b', 'm', 'e', 's')
        self.uni = frequency.NormalProb();self.bi = frequency.NormalProb();self.tri = frequency.NormalProb()
        # self.uni = frequency.AddOneProb();self.bi = frequency.AddOneProb();self.tri = frequency.AddOneProb()

    def idiv(self, v1, v2):
        if v2 == 0:
            return 0
        return float(v1)/v2

    def train(self, data,new_para = True):
        for sentence in data:
            window = [('', 'BOS'), ('', 'BOS')]
            self.bi.add((('', 'BOS'), ('', 'BOS')), 1)
            self.uni.add(('', 'BOS'), 2)
            for word, tag in sentence:
                window.append((word, tag))
                self.uni.add((word, tag), 1)
                self.bi.add(tuple(window[1:]), 1)
                self.tri.add(tuple(window), 1)
                window.pop(0)
        # 这里使用 TnT 标注器的平滑数据
        if new_para:
        #训练集足够大，重新训练参数
            tl1 = 0.0
            tl2 = 0.0
            tl3 = 0.0
            items = sorted(self.tri.samples(), key=lambda x: self.tri.get(x)[1])
            for now in items:
                c3 = self.idiv(self.tri.get(now)[1]-1, self.bi.get(now[:2])[1]-1)
                c2 = self.idiv(self.bi.get(now[1:])[1]-1, self.uni.get(now[1])[1]-1)
                c1 = self.idiv(self.uni.get(now[2])[1]-1, self.uni.getsum()-1)
                # 计算2阶Hmm的三个参数
                if c3 >= c1 and c3 >= c2:
                    tl3 += self.tri.get(now)[1]
                elif c2 >= c1 and c2 >= c3:
                    tl2 += self.tri.get(now)[1]
                elif c1 >= c2 and c1 >= c3:
                    tl1 += self.tri.get(now)[1]
            #正则化参数
            self.l1 = self.idiv(tl1, tl1+tl2+tl3)
            self.l2 = self.idiv(tl2, tl1+tl2+tl3)
            self.l3 = self.idiv(tl3, tl1+tl2+tl3)
        else:
            # 采用默认参数
            self.l1,self.l2,self.l3 = 0.0999899024039,0.311842406398,0.588167691198
    def log_prob(self, s1, s2, s3):
        '''
        *求概率
        * @ param s1 前2个状态
        * @ param s2 前1个状态
        * @ param s3 当前状态
        * @ return 序列的概率 P(s3|s1,s2) =  l1*P(s3) + l2*P(s3|s2) + l3*P(s3,(s2,s1))
        '''
        uni = self.l1*self.uni.freq(s3)
        bi = self.idiv(self.l2*self.bi.get((s2, s3))[1], self.uni.get(s2)[1])
        tri = self.idiv(self.l3*self.tri.get((s1, s2, s3))[1],self.bi.get((s1, s2))[1])
        if uni+bi+tri == 0:
            return float('-inf')
        return log(uni+bi+tri)

    def tag(self, data):
        '''解码部分，动态规划解码'''
        now = [((('', 'BOS'), ('', 'BOS')), 0.0, [])]
        for w in data:
            stage = {}
            flag = True
            for s in self.status:
                if self.uni.freq((w, s)) != 0:
                    flag = False
                    break
            if flag:
                for s in self.status:
                    for pre in now:
                        stage[(pre[0][1], (w, s))] = (pre[1], pre[2]+[s])
                now = list(map(lambda x: (x[0], x[1][0], x[1][1]),stage.items()))
                continue
            for s in self.status:
                for pre in now:
                    p = pre[1]+self.log_prob(pre[0][0], pre[0][1], (w, s))
                    if (not (pre[0][1],(w, s)) in stage) or p > stage[(pre[0][1],(w, s))][0]:
                        stage[(pre[0][1], (w, s))] = (p, pre[2]+[s])
            now = list(map(lambda x: (x[0], x[1][0], x[1][1]), stage.items()))
        return zip(data, max(now, key=lambda x: x[1])[2])
    
    def tag2(self,data):
        first = {}
        now = {}
        link = [] #第i个节点在前一个状态是s，当前状态是t时，前2个状态的tag的值
        tag = {}
        if len(data)==0:
            return []
        if len(data)==1:
            return [(data,'s')]
            
        for i in range(len(data)):
            row = []
            for j in range(4):
                col = []
                for k in range(4):
                    col.append(0)
                row.append(col)
            link.append(row)
        for s in range(4):
            p = float('-inf') if s==1 or s==2 else self.log_prob(('', 'BOS'),('', 'BOS'),(data[0],self.status[s]))
            first[s] = p
        for f in range(4):
            for s in range(4):
                p = first[f] + self.log_prob(('','BOS'),(data[0],self.status[f]),(data[1],self.status[s]))
                now[(f,s)] = p
                link[1][f][s] = f
                
        pre = {}
        for i in range(2,len(data)):
            tmp = copy.deepcopy(pre)
            pre = copy.deepcopy(now)
            now = copy.deepcopy(tmp)
            for s in range(4):
                for t in range(4):
                    now[(s,t)] = -1e20
                    for f in range(4):
                        p = pre[(f,s)] + self.log_prob((data[i-2],self.status[f]),(data[i-1],self.status[s]),(data[i],self.status[t]))
                        if p>now[(s,t)]:
                            now[(s,t)] = p
                            link[i][s][t] = f
        
        score = float('-inf')
        s,t = 0,0
        for i in range(4):
            for j in range(4):
                if now[(i,j)]>score:
                    score = now[(i,j)]
                    s = i;t = j
        for i in range(len(data)-1,-1,-1):
            tag[i] = self.status[t]
            f = int(link[i][s][t])
            t = s;s = f
        return [(data[i],tag[i]) for i in range(len(tag))]
    

        
        