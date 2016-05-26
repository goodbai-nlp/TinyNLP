#!/usr/bin/env python
# encoding: utf-8
# coding: utf-8
"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: FullSegmentation.py
@time: 16-4-18 下午9:30
"""
import time
class FullSegmentation(object):

    def __init__(self):
        self.dict = {}
        self.MAXN_WORD_LENGTH = 10
        self.res = []

    def LoadDict(self):
        file = open('vocab.txt')
        for line in file:
            self.dict[(line.decode(encoding='utf-8').strip())] = len(line)
        print 'dictionary imported,%s words'%len(self.dict)

    def FullSeg(self,root):
        target = root.value[-1]
        if len(target)<=1:
            return root
        for i in range(0,min(len(target),self.MAXN_WORD_LENGTH)):
            res = root.value[:-1]
            front = target if (i==len(target)-1) else target[:i+1]
            post = [] if (i==len(target)-1) else target[i+1:]
            tmp = ''.join(front)
            if tmp in self.dict:
                res.append(front),res.append(post)
                root.add_child(TreeNode(res))
        tres = root.value[:-1]
        front = target[:1]
        post = target[1:]
        tres.append(front), tres.append(post)
        root.add_child(TreeNode(tres))

        for item in root.children:
            self.FullSeg(item)

    def dfs(self,root):
        if len(root.children)==0:
            s = ''
            for item in root.value:
                if(len(item)):
                    s += ''.join(item)+' '
            self.res.append(s)
        for item in root.children:
            self.dfs(item)

class TreeNode(object):

    def __init__(self,value):
        self.value = value
        self.children = []

    def add_child(self,*child):
        self.children+=child

    def show(self,layer):
        print "  "*layer + self.value
        map(lambda child: child.show(layer + 1), self.children)

print time.strftime('%Y-%m-%d %H:%M:%S')
m = FullSegmentation()
m.LoadDict()
root  = TreeNode([list(u'在和平共处五项原则的基础上努力发展同世界')])
m.FullSeg(root)
m.dfs(root)
tmp = m.res[0]
for item in m.res:
    tmp = tmp if(len(tmp)<len(item)) else item
print tmp.strip()
print time.strftime('%Y-%m-%d %H:%M:%S')

