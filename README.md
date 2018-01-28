# NLP2

本项目为BIT NLP作业二

## 项目介绍

本项目实现自动文摘和关键词、短语提取功能，基于TextRank算法实现。

## 代码组织

 * Keysente.py实现自动文摘
 
 * Keyword.py实现关键词、短语提取
 
 * Similarity.py实现判断句子相似、词语相似功能
 
 * Pagerank.py实现pagerank算法
 
 ## 其他文件
 
 * stopwords.txt为关键词提取中的停用词
 
 * wn-data-cmn.tab为中文wordnet数据库
 
 * test.txt为测试文件，编码格式只接受UTF-8
 
 ## 使用方法
 
 自动文摘
 ```
 >>> from Keysente import KeysenteEx
 >>> k = KeysenteEx()
 >>> k.docsummary('test.txt', threshold = 0.01, Keynum = 3)
 ```
 
 关键词提取与关键词组提取
 
 ```
 >>> from Keyword import KeywordEx
 >>> k = KeywordEx()
 >>> k.keyword('test.txt', window = 5, Keynum = 5)
 >>> k.keyphrase('test.txt', window = 5, Keynum = 5)
 ```
  
 ## 参数说明
 
 * test.txt为文档名，函数只接受UTF-8编码的文档
 
 * threshold为阈值，当两节点相似程度大于该值时，在两节点之间加边，默认值为0.01
  
 * Keynum为返回的关键语句/词的数量，在关键词组提取中，该值决定在Keynum + 10个关键字中寻找关键词组，该值与返回的关键词组的数量没有绝对关系
 
 * window为共现窗口的大小，默认为5
 
 
