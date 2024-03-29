# 几种常见分词系统的比较
##概述
中文自然语言处理最首要的就是要中文分词了，现在而言效果最好的还是要算crf了，好用的系统可以查看Stanford NLP，但crf的缺点也是明显的，如模型体积大占内存多，速度慢，无法修改等，所以其他的分词系统虽然不如crf效果好，但也不是完全废掉的，所以这里将对如下系统做分析：  
1. N-最短路分词（ICTCLAS所用的基层模型）  
2. hmm+字典分词 (jieba分词所用的核心模型)  
3. TnT分词 (2阶HMM的演化版)  
4. crf分词 (这里采用的是crf++工具包，Stanford核心模型)  

##模型简介

###N-最短路分词
N-最短路分词是中科院分词系统ICTCLAS中用来做基础分词的核心模块。  
核心思想是：根据词典，找出字串中所有可能的词，构造词切分有向无还图，每个词对应图中的一条边。并赋予边一定的权重（这里有机关）。然后求出该图从起点到终点排名前N的最短路径。  
N-最短路径并不会直接给出分词的最终结果，而是给出一些可能的结果，再由后续的程序继续处理，最后得出最终结果。  
N-最短路径的一个优点就是召回率十分的高，论文中的结果平均在99.5%以上。  
[注]：由于个人没有查明ICTCLAS的权重的详细计算方法，所以只是以词频来衡量权重，这里可能欠妥  

###hmm+字典分词
hmm+字典分词是jieba分词系统的核心模块，这里就不再介绍hmm模型了，主要分析下特点：hmm模型的一个优点就是具有一定的新词发现能力，这也是Character-Based Generative Model的共有特性，实验中发现hmm模型可以识别一些字典里没有的人名和地名；但hmm模型也存在问题，hmm会错误的将不相关的词连到一起，考量其优点和缺点，我们最后决定放弃hmm的新词发现功能，采用hmm+字典进行分词，用字典去做基础的切分，hmm来处理歧义，取得了还算不错的效果。  
[注]：由于放弃了hmm的新词发现能力，所以未登录词只能通过别的方式来解决；实战中发现hmm处理歧义的能力没有想象中那么理想。  

###TnT分词
当我们发现一阶hmm不够用时，直观的想可以考虑采用二阶hmm来提高正确率，这里参照的是A00-1031这篇论文的Trigrams'n'Tags（TnT）模型，TnT模型的公式写起来想这样：  
	`argmax(ΠP(wordi∣tagi)∗P(tagi∣tagi−1,tagi−2))`  
考虑到每个字的标签同样可以加入计算，所以这算是一个TnT的变种，既考虑了已知序列，也考虑了标注序列，它的概率公式写起来像是这样：  
	`argmax(ΠP((wordi,tagi)∣(wordi−1,tagi−1),(wordi−2,tagi−2)))`  
看起来像是TnT和普通n-gram的综合，所以效果应该会比以上的模型好一点  
[注]：大概还有许多的细节的优化和数据平滑的不到位导致实验结果和论文的结果有差距，以后有时间会继续做调整。  
###crf分词
这里采用的是crf++工具包，里面的很多内容还没有完全吃透，只做了性能分析和评测  

##测试集
这里采用的是Bakeoff 2005的测试集，数据主要是由北京大学，微软亚洲研究院，香港城市大学，台湾中央研究院提供，主要在pku和msr两个测试集上做的评测。评测脚本采用的是测试集里带的perl脚本。  
主要评分项目如下：
```
    === SUMMARY:
    === TOTAL INSERTIONS: 9274
    === TOTAL DELETIONS: 1365
    === TOTAL SUBSTITUTIONS: 8377
    === TOTAL NCHANGE: 19016
    === TOTAL TRUE WORD COUNT: 104372
    === TOTAL TEST WORD COUNT: 112281
    === TOTAL TRUE WORDS RECALL: 0.907
    === TOTAL TEST WORDS PRECISION: 0.843
    === F MEASURE: 0.874
```

##性能评测

鉴于n-最短路径分词只做了基础部分，缺少后续处理，还不能评测其精确率和召回率，这里只对后三个分词系统性能进行评估，评估采用的测试集为pku和msr的测试集。  
实验机型：  
Intel core-I3  
2.4 GHZ  
####分词准确度：
|   准确度分析      |hmm+字典 |  TnT  |  crf  |
|-------- |--------|-------|-------|
|pku-精确率|    0.917  |0.925|0.923
|pku-召回率|0.926 |0.931|0.937|
|  pku-F  |0.921|0.928|0.930|
|msr-精确率|0.923|0.930|0.964|
|msr-召回率|0.901|0.946|0.965|
|  msr-F  |0.912|0.940|0.964|

【注】考虑到泛化能力，hmm+字典在切换训练语料时并没有添加特别针对语料的字典，所以在msr语料上的效果还不如pku  
TnT和crf在得到了更大规模的预料后性能都有了明显的提升，按照论文TnT的理论F值应该在95%左右。
####分词错误总结
|    错误分析     |hmm+字典 |  TnT  | crf   |
|:---------|--------|-------|-------|
|pku-误成词|    3289   |2559|1500|
|pku-误拆词|	2188	|1913|3122|
|msr-误成词|	4773	|3086|1412|
|msr-误拆词|	2164	|1401|1305|
【注】从表中容易看出，1）TnT和crf的误成词和误拆词数目明显少于hmm+字典，这也是模型的新词发现能力的体现。2）通过对比TnT和crf，可以发现TnT的误成词数量明显高于crf，而误拆词的数目和crf基本相近，在pku语料中还取得了比crf更好的效果，这也为之后分词系统的优化方向提供了一些思路
####分词速度
|    分词速度     |hmm+字典 |  TnT  |  crf  |
|-------- |--------|-------|-------|
|	字/秒	  |		4.4万   |1696   |   2.5万    |
【注】由于TnT模型是用纯python写的，有的地方为了追求代码的简单而放弃了时间复杂度，所以性能相对较差，但从理论上分析TnT的模型应该是比crf要简单一些的（TnT本质上还是马尔科夫链，crf既有前面的节点没还有后面的节点），如果同属c语言编写，TnT的速度应该高于crf，TnT的代码优化也是之后的工作之一。
####模型训练时间（pku）
|    模型训练     |hmm+字典 |  TnT  |  crf  |
|-------- |--------|-------|-------|
|	秒	  |		11   |	 25  |    50分钟   |
####OOV率
|   OOV分析      |hmm+字典 |  TnT  |  crf  |
|-------- |--------|-------|-------|
|  pku  |0.058	|0.607|0.566|
|  msr  |0.168	|0.375|0.661|
【注】hmm+字典的新词发现能力很弱，几乎为0  
	 TnT和crf模型的新词发现能力很强，oov率很高，TnT在msr语料中的oov率甚至还超过了crf。
####加上NER后的准确度
|   准确度分析      |hmm+字典 |  TnT  |  crf  |
|-------- |--------|-------|-------|
|pku-精确率|    0.901  |0.927|-|
|pku-召回率|	0.937  |0.931|-|
|  pku-F  |	0.927  |0.929|-|
|msr-精确率|	0.910 |0.933|-|
|msr-召回率|	0.923|0.948|-|
|  msr-F  |0.916|0.940|-|
【注】加入了人名和地名识别后，hmm+字典模型有了一些提升，由于ner模型并不是很好，所以提升并不是十分明显，平衡了精确率和召回率后大概只提升了0.06.而对于已经具有一定新词发现能力的crf和TnT,提升也不是十分明显。
##总结
###hmm+字典
从上面的表格中可以轻易看出，hmm+字典在准确率和召回率是不及其它两个模型的，从求解公式就可以得出。   hmm+字典的优势在于  
	1）模型简单，容易理解和修改，训练时间较短  
    2）分词速度快，这点在实时性要求较高时很有用  
    3）支持用户字典。中文分词受语料本身的影响很大，某些情况下我们可能希望通过人工添加来提高正确率，这是其他两个模型所做不到的  
【总】hmm+字典适合精确度要求一般，分词速度要求较高，要求支持用户自定义字典的环境  
###TnT
TnT模型介于hmm+字典和crf之间，无论是精确度还是模型复杂度，它的优势是：  
	1）相比于hmm+字典，它的模型相对复杂，这也给了它更高的精确度、召回率以及不错的新词识别能力  
	2）虽然精确度不如crf，但是TnT模型更易修改，模型的大小也比crf小很多，这在实际生产中也是要有用的  
【总】TnT模型介于hmm+字典和crf之间，当内存资源相对紧缺，分词准确率要求也较高时可以采用  
###crf
crf是目前公认比较强的分词模型，它的精确率和召回率都是三者中最好的。  
	1）crf优点：准确率高，召回率高  
    2）crf缺点：对应于高准确率，crf的模型复杂度很高，它的训练需要很长时间，在我的电脑上跑了（）分钟，crf模型很大，训练好的模型达百M，这个体积有时是难以接受的  
【总】crf模型的实验结果是最好的，公认的比较好的模型，但也存在问题，需要生产中按需解决。  

上述三种模型在实际的项目中均有使用，简单的模型通过分层和叠加同样可以达到复杂模型的效果，根据实际的需求去选择合适的模型才是合理的做法。  
##参考文献
[1] TnT -- A Statistical Part-of-Speech Tagger -- Thorsten Brants（A00-1031）  
[2] A Character-Based Joint Model for Chinese Word Segmentation --Wang (C10-1132)  
[3] Which is More Suitable for Chinese Word Segmentation,the Generative Model or the Discriminative One? --wang(Y09-2047)  
[4] 基于N-最短路径方法的中文词语粗分模型--张华平  