#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: test.py
@time: 16-7-24 下午3:49
"""
from dataset import read_dataset2

if __name__ == '__main__':
    f = open('nametest.txt','wb')
    train_data = read_dataset2()
    for sentence in train_data:
        res = ''
        ttmp = ''
        if "/nr" in sentence:
            index = 0
            sen = sentence.split()
            while index < len(sen):
                words = sen[index]
                word1, tag1 = words.rsplit('/', 1)[0], words.rsplit('/', 1)[1]
                if (tag1 == 'nr'):
                    if (index < len(sen) - 1):
                        words = sen[index + 1]
                        word2, tag2 = words.rsplit('/', 1)[0], words.rsplit('/', 1)[1]
                        if (tag2 == 'nr'):
                            ttmp += (word1+word2+' ')
                            index+=1
                index+=1
            
        res += (ttmp+'\n')
        f.write(res.encode('utf-8'))
    f.close()