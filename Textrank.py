from Similarity import simi
from Pagerank import pagerank
import networkx as nx

class rank:
    def __init__(self):
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

        for i in range(len(self.sentens) - 1):
            G.add_node(i)
        return G

    def Addedge(self, G, threshold = 0.01):

        '''
        Add edges to the graph
        
        :param G: The graph need to add edges
        :param threshold: Deciding whether a edge should be added
        :return: The graph with edges added
        '''
        for sentelead in G:
            for senteflo in G:
                if simi(self.sentens[sentelead], self.sentens[senteflo]) > threshold and sentelead != senteflo:
                    G.add_edge(sentelead, senteflo, weight = simi(self.sentens[sentelead], self.sentens[senteflo]))
        return G
    def docsummary(self, doc, threshold = 0.01, Keynum = 3):
        G = nx.Graph()
        self.Addnode(doc, G)
        self.Addedge(G, 0.01)
        G_pagerank = pagerank(G)
         # Find out the most important sentences
        keyphrase = sorted(G_pagerank, key=G_pagerank.get, reverse=True)
        try:
            for i in range(Keynum):
                print(self.sentens[keyphrase[i]])
        except IndexError:
            print('The doc must have more than three sentences')
if __name__ == '__main__':
    ranking = rank()
    ranking.docsummary('test1.txt')


        




        
    


