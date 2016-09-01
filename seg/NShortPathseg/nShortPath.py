#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: nShortPath.py
@time: 16-9-1 上午9:54
"""

from graph.wordnet import WordNet
import copy



class NShotPath(object):

    def __init__(self):
        pass

    def seg(self, sentence, n):

        if not sentence:
            return sentence

        stack = []
        path = []
        word_net = WordNet(sentence)

        last_node = word_net.get_last()
        stack.append(last_node)
        current_node = last_node

        while stack:
            while current_node!=0:
                first_node = word_net.get_vertex(current_node).get_current_node()

                stack.append(first_node)
                current_node = first_node

            path.append(copy.deepcopy(stack))


            current_node = stack.pop()

            while True:
                current_vertex = word_net.get_vertex(current_node)

                if not stack:
                    break

                if not current_vertex.has_pre() and stack:
                    current_node = stack.pop()
                    continue

                else:
                    stack.append(current_node)
                    current_node = current_vertex.pop_pre()
                    stack.append(current_node)
                    break
        return path


if __name__ == '__main__':
    sentence = u'他说的确实在理'
    segment = NShotPath()
    path = segment.seg(sentence, 3)
    for p in path :
        p = sorted(p)
        set = ''
        for index in range(len(p)-1):
            set+=sentence[p[index]:p[index+1]]+'/'
        print set