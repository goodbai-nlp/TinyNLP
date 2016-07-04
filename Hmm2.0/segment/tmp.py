#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: muyeby
@contact: bxf_hit@163.com
@site: http://muyeby.github.io
@software: PyCharm
@file: tmp.py
@time: 16-7-4 下午8:36
"""
#!/usr/bin/python
# coding:utf-8
"""
  @author royguo1988@gmail.com
  @date 2012-12-23
"""
class Node(object):
  """有向图中的节点"""
  def __init__(self,word):
    # 当前节点作为左右路径中的节点时的得分
    self.max_score = 0.0
    # 前一个最优节点
    self.prev_node = None
    # 当前节点所代表的词
    self.word = word
class Graph(object):
  """有向图"""
  def __init__(self):
    # 有向图中的序列是一组hash集合
    self.sequence = []
class DPSplit(object):
  """动态规划分词"""
  def __init__(self):
    self.dict = {}
    self.words = []
    self.max_len_word = 0
    self.load_dict('dict.txt')
    self.graph = None
    self.viterbi_cache = {}
  def get_key(self, t, k):
    return '_'.join([str(t),str(k)])
  def load_dict(self,file):
    with open(file, 'r') as f:
      for line in f:
        word_list = [w.encode('utf-8') for w in list(line.strip().decode('utf-8'))]
        if len(word_list) > 0:
          self.dict[''.join(word_list)] = 1
          if len(word_list) > self.max_len_word:
            self.max_len_word = len(word_list)
  def createGraph(self):
    """根据输入的句子创建有向图"""
    self.graph = Graph()
    for i in range(len(self.words)):
      self.graph.sequence.append({})
    word_length = len(self.words)
    # 为每一个字所在的位置创建一个可能词集合
    for i in range(word_length):
      for j in range(self.max_len_word):
        if i+j+1 > len(self.words):
          break
        word = ''.join(self.words[i:i+j+1])
        if word in self.dict:
          node = Node(word)
          # 按照该词的结尾字为其分配位置
          self.graph.sequence[i+j][word] = node
    # 增加一个结束空节点，方便计算
    end = Node('#')
    self.graph.sequence.append({'#':end})
    # for s in self.graph.sequence:
    #   for i in s.values():
    #     print i.word,
    #   print ' - '
    # exit(-1)
  def split(self, sentence):
    self.words = [w.encode('utf-8') for w in list(sentence.decode('utf-8'))]
    self.createGraph()
    # 根据viterbi动态规划算法计算图中的所有节点最大分数
    self.viterbi(len(self.words), '#')
    # 输出分支最大的节点
    end = self.graph.sequence[-1]['#']
    node = end.prev_node
    result = []
    while node:
      result.insert(0,node.word)
      node = node.prev_node
    print ''.join(self.words)
    print ' '.join(result)
  def viterbi(self, t, k):
    """第t个位置，是单词k的最优路径概率"""
    if self.get_key(t,k) in self.viterbi_cache:
      return self.viterbi_cache[self.get_key(t,k)]
    node = self.graph.sequence[t][k]
    # t = 0 的情况,即句子第一个字
    if t == 0:
      node.max_score = self.lm.get_init_prop(k)
      self.viterbi_cache[self.get_key(t,k)] = node.max_score
      return node.max_score
    prev_t = t - len(k.decode('utf-8'))
    # 当前一个节点的位置已经超出句首，则无需再计算概率
    if prev_t == -1:
      return 1.0
    # 获得前一个状态所有可能的汉字
    pre_words = self.graph.sequence[prev_t].keys()
    for l in pre_words:
      # 从l到k的状态转移概率
      state_transfer = self.lm.get_trans_prop(k, l)
      # 当前状态的得分为上一个最优路径的概率乘以当前的状态转移概率
      score = self.viterbi(prev_t, l) * state_transfer
      prev_node = self.graph.sequence[prev_t][l]
      cur_score = score + prev_node.max_score
      if cur_score > node.max_score:
        node.max_score = cur_score
        # 把当前节点的上一最优节点保存起来，用来回溯输出
        node.prev_node = self.graph.sequence[prev_t][l]
    self.viterbi_cache[self.get_key(t,k)] = node.max_score
    return node.max_score
def main():
  dp = DPSplit()
  dp.split('中国人民银行')
  dp.split('中华人民共和国今天成立了')
  dp.split('努力提高居民收入')
if __name__ == '__main__':
  main()