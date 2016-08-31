#!/usr/bin/env python
# encoding: utf-8
"""
@version: V0.1
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: NumNer.py
@time: 16-7-27 下午3:34
"""
import re
class NumRec(object):
    def __init__(self):
        self.separator = ' '
    def NumNer(self,sentence):
        '''特殊处理数字'''
        seg = []
        # print 'before:',' '.join(sentence)
        for word in sentence:
            re_han = re.compile(ur"([\u4E00-\u9FA5\u25cb]+)")
            re_skip = re.compile(ur"^[\uff0d\-{0,1}a-zA-Z0-9\uff10-\uff19\u2014\uff21-\uff3a\uff41-\uff5a\u2026\u25cb\\.]$")
            blks = re_han.split(word)
            tmp = []
            for item in blks:
                if item:
                    if re_han.match(item):
                        tmp.append(item)
                    else:
                        i = 0
                        while i < len(item):
                            ttmp = ''
                            if not re_skip.match(item[i]):
                                tmp.append(item[i])
                                i += 1
                            else:
                                while (i < len(item)) and re_skip.match(item[i]):
                                    ttmp += item[i]
                                    i += 1
                                tmp.append(ttmp)
            seg+=tmp
        # ss  = separator.join(seg)
        # print 'Mid:',ss
    
        re_CN_NUM = re.compile(ur"^[\uff0d\-]{0,1}[0-9a-zA-Z\uff10-\uff19\u25cb\\.\u5341\u767e\u5343\u4e07\u4ebf\/]+$")
        re_B_NUM = re.compile(ur"^[\u25cb\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343\u4e07\u4ebf\u5206\u4e4b\u70b9]+$")
        re_date_time = re.compile(ur"^[\u5e74\u6708\u65e5\u5341\u767e\u5343\u4e07\u4ebf\uff05\u65f6\u5206]$")
        
        i = 0
        while i < (len(seg) - 1):
            tmp = ''
            if (re_B_NUM.match(seg[i]) or re_CN_NUM.match(seg[i])):
                tmp += seg[i]
                j = 0
                for j in range(i + 1, len(seg)):
                    if not (re_B_NUM.match(seg[j]) or re_CN_NUM.match(seg[j])):
                        break
                    tmp += seg[j]
                res = self.separator.join(seg[:i]) + self.separator + tmp + self.separator + self.separator.join(seg[j:])
                seg = res.split(self.separator)
            i += 1
        # print '汉字join:', ' '.join(seg)
        i = 0
        while i < (len(seg)):
            tmp = ''
            if re_CN_NUM.match(seg[i]) or re_B_NUM.match(seg[i]):
                tmp += seg[i]
                if (i + 2 <= len(seg) and re_date_time.match(seg[i + 1])):
                    tmp += seg[i + 1]
                    res = self.separator.join(seg[:i]) + self.separator + tmp + self.separator + self.separator.join(seg[i + 2:])
                    seg = res.split(self.separator)
                    i = i + 1
                    continue
            i = i + 1
        # ss = separator.join(seg)
        # print 'After:',ss
        return seg
