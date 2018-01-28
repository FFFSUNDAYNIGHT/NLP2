import networkx as nx
import jieba.posseg as p
import re
from jieba import cut
from Pagerank import pagerank

class KeywordEx:
    '''
    Key word extraction
    '''

    def __init__(self):
        self.sentens = []
        self.word = []
        self.Keyword = []
        #self.Wordfilter = []
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
        # Part of speech filter, only noun, verb, adjective can be added to the graph
        POSre = re.compile('[nav].*')
        with open(doc, 'r', encoding='utf8') as f:
            content = f.read().replace('\ufeff','')
            content = content.replace('\n','')
            self.sentens = content.split('。')
        self.sentens.remove('')
        # Wordfilter is a list of stopword
        # Include punctuations
        for sente in self.sentens:
            sente = list(p.cut(sente))
            for word, flag in sente:
                if word not in Wordfilter and POSre.fullmatch(flag) is not None:
                    self.word.append(word)
                else:
                    pass
        G.add_nodes_from(self.word)
        # Add edges where words are in the same window
        for i in range(len(self.word) - window + 1):
            for j in range(i + 1, i + window):
                # Every edge's weight is set to be one at the begining
                G.add_edge(self.word[i], self.word[j], weight = 1)
    
    def keywordex(self, doc, window = 5, Keynum = 5):
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
        self.keywordex(doc = doc, window = window, Keynum = Keynum + 10)
        keywordset = set(self.Keyword)
        keyphrset = set()
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
            if len(phraseword) > 1:
                keyphrset.add(''.join(phraseword))
        return [phrase for phrase in keyphrset]
if __name__ == '__main__':
    key = KeywordEx()
    print('Please input file name:', end='')
    s = input()
    print(key.keywordex(s, window = 5, Keynum = 5))
    print(key.keyphrase(s))





        