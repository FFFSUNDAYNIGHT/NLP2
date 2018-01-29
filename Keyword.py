import networkx as nx
import jieba.posseg as p
import re
from jieba import cut
from Pagerank import pagerank
from Similarity import wordsim

class KeywordEx:
    # Key word extraction class

    def __init__(self):
        self.sentens = []
        self.word = []
        self.Keyword = []
    def Readfilter(self, filter = 'stopwords.txt'):
        '''
        Load stop words from 'stopwords.txt' into Wordfilter
        '''
        Wordfilter = []
        with open(filter,'r',encoding='utf8') as f:
            lines = f.readlines()
            lines[0] = lines[0].replace('\ufeff','')
        for line in lines:
            Wordfilter.append(line.replace('\n',''))
        return Wordfilter

    def Constrgra(self, doc, G, window = 2, Wordfilter = []): 
        '''
        Construct graph based on documention's words
        :param doc: The documention to cope with
        :param G: The origin graph
        :param window: The size of 'co-occurrence' window
        :param Wordfilter: Filter the stop word. Default to an empty list
        :return: A graph with nodes and edges added
        '''
        # Part of speech filter, only noun, verb, adjective, adverb can be added to the graph
        POSre = re.compile('[navd].*')
        with open(doc, 'r', encoding='utf8') as f:
            content = f.read().replace('\ufeff','')
            content = content.replace('\n','')
            self.sentens = content.split('。')
        self.sentens.remove('')
        # Wordfilter is a list of stopwords
        # Include punctuations
        for sente in self.sentens:
            sente = list(p.cut(sente))
            for word, flag in sente:
                if word not in Wordfilter and POSre.fullmatch(flag) is not None:
                    self.word.append(word)
                else:
                    pass
        G.add_nodes_from(self.word)
        # Add edges where words are in the same 'co-occurrence' window
        for i in range(len(self.word) - window + 1):
            for j in range(i + 1, i + window):
                # Every edge's weight is set to be one at the begining
                G.add_edge(self.word[i], self.word[j], weight = 1)
        # Find out similar words
        for word1 in list(G):
            for word2 in list(G):
                if word1 or word2 is None:
                    pass
                    # if two words are similar, then wordsim(word1, word2) return 0.9
                elif wordsim(word1, word2) == 0.9:
                    # 将word2节点的所有节点连至word1节点
                    # 删除word2节点
                    edge_to_add = []
                    word2_edges = G.edges([word2])
                    for word2, word in word2_edges:
                        edge_to_add.append((word1, word))
                    G.remove_node(word2)
                    G.add_edges_from(edge_to_add)
    def keyword(self, doc, window = 5, Keynum = 5):
        '''
        Key word extraction
        :return: Keynum key words
        '''
        g = nx.Graph()
        Wordfilter = self.Readfilter()
        self.Constrgra(doc, g, window = window, Wordfilter = Wordfilter)
        G_pagerank = pagerank(g)
        # sorted G_pagerank to get the most important words
        Keyword = sorted(G_pagerank, key = G_pagerank.get, reverse=True)
        try:
            self.Keyword = Keyword[:Keynum]
            return Keyword[:Keynum]
        except IndexError:
            print('The doc must have more than 5 words')
    
    def keyphrase(self, doc, window = 5, Keynum = 5):
        # Return the Key phrases according to the keyword list
        self.keyword(doc = doc, window = window, Keynum = Keynum + 10)
        keywordset = set(self.Keyword)
        keyphrset = set()
        # 如果n关键词在原文中是邻接的
        # 则将这n个关键词作为关键短语
        for sente in self.sentens:
            phraseword = []
            sente = list(cut(sente))
            for word in sente:
                if word in keywordset:
                    phraseword.append(word)
                elif len(phraseword) > 1:
                    keyphrset.add(''.join(phraseword))
                    phraseword = []
                else:
                    phraseword = []
            # 检测最后一个词是否和前一个词构成关键词组
            if len(phraseword) > 1:
                keyphrset.add(''.join(phraseword))
        return [phrase for phrase in keyphrset]
if __name__ == '__main__':
    key = KeywordEx()
    print('Please input file name:', end='')
    s = input()
    print(key.keyword(s, window = 5, Keynum = 5))
    print(key.keyphrase(s))





        