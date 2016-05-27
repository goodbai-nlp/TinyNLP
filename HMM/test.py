# encoding=utf-8
import hmm
f2 = open('output.txt','wb')
for line in open('pku_test.utf8','rb'):
	seg_list = hmm.cut(line)
	s = ' '.join(seg_list).encode('utf-8')
	s+='\n'
	f2.write(s)
# sentence_list = [
# "姚晨和老凌离婚了",
# "他说的确实在理",
# "长春市长春节讲话"
# ]
# print u"=默认效果"
#
# for sentence in sentence_list:
# 	seg_list = finalseg.cut(sentence)
# 	print "/ ".join(seg_list)
#
# print u"\n=打开新词发现功能后的效果\n"
#
#
# for sentence in sentence_list:
# 	seg_list = finalseg.cut(sentence,find_new_word=True)
# 	print "/ ".join(seg_list)

