#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: coredictionary.py
@time: 16-9-1 上午10:12
"""

import codecs
import os
from singlenton import Singleton
CORE_DICTIONARY_PATH = os.getcwd()+'/dictionary/dict.txt'

class Dictionary(object):
    __metaclass__ = Singleton
 
    def __init__(self):
        self.dictionary = {}
        self.init_dictionary()


    def init_dictionary(self):
        with codecs.open(CORE_DICTIONARY_PATH, 'r', encoding='utf-8') as df:
            for lin in df.readlines():
                lin = lin.strip('\n')
                lin = lin.split('\t')
                self.dictionary[lin[0]] = lin[1:]


    def is_in_dictionary(self, word):
        return word in self.dictionary.keys()


    def get_word_info(self, word):
        return self.dictionary.get(word, None)

    def __iter__(self):
        return iter(self.dictionary.keys())




if __name__ == '__main__':
    import json

    d = Dictionary()
    print json.dumps(d.dictionary, ensure_ascii=False, indent=4)
