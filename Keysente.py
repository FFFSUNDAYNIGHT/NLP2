from Similarity import simi
from Pagerank import pagerank
import networkx as nx

class KeysenteEx:
    def __init__(self):
        self.threshold = 0.01
        self.sentens = []

    def Addnode(self, doc, G):
        '''
        Add node to the graph according to the doc's sentences
        :param doc: The doc need to cope with
        :param G: The origin graph
        :return: The graph with nodes added
        '''
        with open(doc, 'r', encoding='utf8') as f:
            content = f.read().replace('\ufeff','')
            content = content.replace('\n','')
            self.sentens = content.split('。')
            self.sentens.remove('')
        for i in range(len(self.sentens)):
            G.add_node(i)
        return G

    def Addedge(self, G):
        '''
        Add edges to the graph where the similarity of two sentences > self.threshold
        :param G: The graph need to add edges
        :return: The graph with edges added
        '''
        for sentelead in G:
            for sentefol in G:
                # sentelead and sentefol are the index of sentens
                if simi(self.sentens[sentelead], self.sentens[sentefol]) > self.threshold and sentelead != sentefol:
                    G.add_edge(sentelead, sentefol, weight = simi(self.sentens[sentelead], self.sentens[sentefol]))
        return G
    def docsummary(self, doc, Keynum = 3):
        '''
        Finish the docsummary job
        :param doc: Same as above
        :param Keynum: The number of sentences to return
        '''
        G = nx.Graph()
        self.Addnode(doc, G)
        self.Addedge(G)
        G_pagerank = pagerank(G)
         # Find out the most important sentences
        keysente = sorted(G_pagerank, key=G_pagerank.get, reverse=True)
        try:
            return [self.sentens[keysente[n]] for n in range(Keynum)]
        except IndexError:
            print('The doc must have more than three sentences')
if __name__ == '__main__':
    keysente = KeysenteEx()
    print('Please input file name:', end='')
    s = input()
    print(keysente.docsummary(s, Keynum = 3))


        




        
    


