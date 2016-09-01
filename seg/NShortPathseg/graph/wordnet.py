#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: wordnet.py
@time: 16-9-1 上午9:55
"""
from __future__ import unicode_literals
import sys
sys.path.append("..")
from vertex import Vertex
from dictionary.coredictionary import Dictionary


class WordNet(object):

    def __init__(self, sentence):
        self.vertexs = {}
        self.size = len(sentence)
        self.sentence = sentence
        self.edges = []
        self.init_net()


    def init_net(self):
        for index in range(self.size+1):
            self.vertexs[index] = Vertex(index)

        for index in range(0, self.size):
            self.add_connect(index, index+1)


        for w in Dictionary():
            if w not in self.sentence:
                continue

            if len(w) == 1:
                continue
            start_index = self.sentence.index(w)
            end_index = start_index+len(w)
            self.add_connect(start_index, end_index)

    def add_connect(self, from_vertex, to_vertex):
        self.edges.append((from_vertex, to_vertex))
        self.vertexs[to_vertex].add_pre(from_vertex)

    def get_last(self):
        return self.size

    def get_vertex(self, vertex_id):
        return self.vertexs[vertex_id]