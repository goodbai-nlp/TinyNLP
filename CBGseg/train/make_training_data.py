#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: make_crf_train_data.py.py
@time: 16-7-22 下午8:10
"""
import codecs
import sys

def character_tagging(input_file, output_file):
    input_data = codecs.open(input_file, 'r')
    output_data = codecs.open(output_file, 'w')
    for line in input_data.readlines():
        if sys.version < '3.0':
            if not (type(line) is unicode):
                try:
                    line = line.decode('utf-8')
                except:
                    line = line.decode('gbk', 'ignore')
        tokens = line.strip().split()
        tmp = (' '.join([t.rsplit('/', 1)[0] for t in tokens]))
        if tmp:
            tmp+="\n"
            output_data.write(tmp.encode('utf-8'))
    input_data.close()
    output_data.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "pls use: python make_snow_train_data.py input output"
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    character_tagging(input_file, output_file)
