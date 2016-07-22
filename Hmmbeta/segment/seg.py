#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: seg.py
@time: 16-7-5 下午3:07
"""
import time
import os
import re
from __init__ import cut
TEST_FILE = os.getcwd()+'/pku_training.utf8'
re_han = re.compile(ur"([\u4E00-\u9FA5]+)")
re_skip = re.compile(ur"^[a-zA-Z0-9]+$")
if __name__ == '__main__':
    i=0
    f = open('./output.txt','wb')
    print time.strftime('%Y-%m-%d %H:%M:%S')
    for line in open(TEST_FILE,'rb'):
        if not (type(line) is unicode):
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('gbk', 'ignore')
        i+=1
        res = ''
        if (i <= 4765):
            blocks = re_han.split(line.strip())
            for blk in blocks:
                if not blk:
                    continue
                if re_han.match(blk):
                    tmp = cut(blk)
                    res += tmp
                elif re_skip.match(blk):
                    res += (' '+blk+' ')
                else:
                    res += blk
        else:
            break
        if(res):
            res+="\n"
            f.write(res.encode('utf-8'))
    print time.strftime('%Y-%m-%d %H:%M:%S')
    f.close()