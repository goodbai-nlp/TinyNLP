#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: vertex.py
@time: 16-9-1 上午9:55
"""

class Vertex(object):
    def __init__(self, id):

        self.id = id
        self.pre_nodes = []
        self.current_index = 0

    def __le__(self, other):
        return self.id <= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

    def __str__(self):
        return str(self.id)

    def add_pre(self, from_pre):
        self.pre_nodes.append(from_pre)
        self.pre_nodes = sorted(self.pre_nodes)

    def get_current_node(self):
        return self.pre_nodes[self.current_index]

    def pop_pre(self):
        if self.current_index>= len(self.pre_nodes)-1:
            return
        else :
            self.current_index+=1
            return self.pre_nodes[self.current_index]

    def has_pre(self):
        if self.current_index >= len(self.pre_nodes)-1:
            return False
        return True