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
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        word_list = line.strip().split()
        for word in word_list:
            if len(word) == 1:
                output_data.write(word + "/s ")
            else:
                output_data.write(word[0] + "/b ")
                for w in word[1:len(word) - 1]:
                    output_data.write(w + "/m ")
                output_data.write(word[len(word) - 1] + "/e ")
        output_data.write("\n")
    input_data.close()
    output_data.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "pls use: python make_snow_train_data.py input output"
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    character_tagging(input_file, output_file)
