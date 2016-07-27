# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import os
import sys
import time
sys.path.append("..")

from utils.tnt import TnT
from model.NumNer import NumNer
from model.y09_2047 import CharacterBasedGenerativeModel
TRAIN_FILE = '../train/data2.txt'
TEST_FILE = 'pku_test.utf8'
TEST_OUTPUT = '../output.txt'
class Seg(object):

    def __init__(self, name='other'):
        if name == 'tnt':
            self.segger = TnT()
        else:
            self.segger = CharacterBasedGenerativeModel()

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

if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    seg = Seg()
    seg.train(TRAIN_FILE)
    f = open(TEST_FILE)
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
        tmp = NumNer(res)
        ans = ' '.join(tmp)
        ans+='\n'
        f2.write(ans.encode('utf-8'))
    print(time.strftime('%Y-%m-%d %H:%M:%S'))