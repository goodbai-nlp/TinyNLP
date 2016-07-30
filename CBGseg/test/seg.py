# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import os
import sys
import time
sys.path.append("..")

from utils.tnt import TnT
from model.NumNer import NumRec
from model.y09_2047 import CharacterBasedGenerativeModel
from model.PlaceNer import PlaceRec
from model.NameNer import CNNAME,decode

TRAIN_FILE = '../train/data/data2.txt'
USER_DICT = '../train/data/userdict.txt'
TEST_FILE = 'pku_test.utf8'
TEST_FILE2 = 'test.txt'
TEST_OUTPUT = '../score/output.txt'

class Seg(object):

    def __init__(self, name='other'):
        if name == 'tnt':
            self.segger = TnT()
        else:
            self.segger = CharacterBasedGenerativeModel()
        self.Pner = PlaceRec()
        self.Numner = NumRec()
        self.cname = CNNAME()
        self.cname.fit()
        self.idict = {}
        self.load_dict()
    
    def load_dict(self):
        f = codecs.open(USER_DICT,'r')
        for line in f:
            if sys.version < '3.0':
                if not (type(line) is unicode):
                    try:
                        line = line.decode('utf-8')
                    except:
                        line = line.decode('gbk', 'ignore')
            word = line.strip()
            self.idict[word]=1
    
    def save(self, fname, iszip=True):
        self.segger.save(fname, iszip)

    def load(self, fname, iszip=True):
        self.segger.load(fname, iszip)

    def train(self, fname):
        fr = codecs.open(fname, 'r', 'utf-8')
        data = []
        for i in fr:
            line = i.strip()
            if not line:
                continue
            tmp = map(lambda x: x.split('/'), line.split())
            data.append(tmp)
        fr.close()
        self.segger.train(data)

    def seg(self, sentence):
        ret = self.segger.tag(sentence)
        res = []
        tmp = ''
        for i in ret:
            if i[1] == 'e':
                res.append(tmp+i[0])
                tmp = ''
            elif i[1] == 'b' or i[1] == 's':
                if tmp:
                    res.append(tmp)
                tmp = i[0]
            else:
                tmp += i[0]
        if tmp:
            res.append(tmp)
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
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    seg = Seg()
    seg.train(TRAIN_FILE)
    f = open(TEST_FILE2)
    f2 = open(TEST_OUTPUT,'wb')
    print('model loaded')
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    for line in f:
        if sys.version < '3.0':
            if not (type(line) is unicode):
                try:
                    line = line.decode('utf-8')
                except:
                    line = line.decode('gbk', 'ignore')
        line = line.strip()
        res = seg.seg(line)
        res1 = seg.Numner.NumNer(res)
        res2 = seg.Pner.Place_Ner(res1)
        namelist = decode(seg.cname,res2)
        res3 = Name_Replace(namelist,res2)
        ans = '\n'.join(res3)
        ans+='\n'
        f2.write(ans.encode('utf-8'))
    print(time.strftime('%Y-%m-%d %H:%M:%S'))

