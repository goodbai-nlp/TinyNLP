#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: hmm++.py
@time: 16-7-3 下午7:41
"""
import numpy as np
import os
import sys
from hmmlearn import hmm
DIR = os.getcwd()+'/../data/'
DICT = DIR + 'jieba_dict.txt'
