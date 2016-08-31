#!/usr/bin/env python
# encoding: utf-8
"""
@version: v0.2
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: PlaceNer.py
@time: 16-7-27 下午9:38
"""
import sys
import re
DICT_DIR = '../train/data/placecontext.txt'
re_han = re.compile(ur"([\u4E00-\u9FA5\u25cb]+)")
class PlaceRec(object):
    
    def __init__(self):
        self.place_context = {}
        self.getdict()
        
    def getdict(self):
        f = open(DICT_DIR,'rb')
        for line in f:
            if sys.version < '3.0':
                if not (type(line) is unicode):
                    try:
                        line = line.decode('utf-8')
                    except:
                        line = line.decode('gbk', 'ignore')
            word = line.strip()
            self.place_context[word] = 1
            
    def Place_Ner(self,sen):
        # print 'before:',' '.join(sen)
        for itm in self.place_context.keys():
            index =0
            while index < len(sen):
                if sen[index] == itm:
                    tmp = ''
                    if index-2>=0 and len(sen[index-1])==1 and len(sen[index-2])==1 and re_han.match(sen[index-1]) and re_han.match(sen[index-2]):
                        if len(itm)<2:
                            tmp = sen[index-2]+sen[index-1]+sen[index]
                            sen = sen[:index-2] + [tmp] + sen[index+1:]
                            # print tmp
                            index -=2
                        # else:
                        #     tmp = sen[index-2]+sen[index-1]
                        #     sen = sen[:index-2] + [tmp] + sen[index:]
                        #     print tmp
                        #     index -=1
                    elif index-1>=0 and len(sen[index-1])==2 and re_han.match(sen[index-2]):
                        if len(itm)<2:
                            tmp = sen[index-1]+sen[index]
                            sen = sen[:index-1] + [tmp] + sen[index+1:]
                            # print tmp
                            index -=1
                        else:
                            pass
                index+=1
        # print 'After:',' '.join(sen)
        return sen