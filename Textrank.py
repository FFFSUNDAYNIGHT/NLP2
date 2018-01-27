from Similarity import simi
from Pagerank import pagerank
import networkx as nx

class rank:
    def __init__(self):
        pass

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
            sentens = content.split('。')
        
        for sente in sentens:
            G.add_node(sente)
        G.remove_node('')
        return G

    def Addedge(self, G, threshold):
    
    '''
    Add edges to the graph

    :param G: The graph need to add edges
    :param threshold: Deciding whether a edge should be added
    :return: The graph with edges added
    '''
        for sentelead in G:
            for senteflo in G:
                if simi(sentelead, senteflo) > threshold and sentelead != senteflo:
                    G.add_edge(sentelead, senteflo, weight = simi(sentelead, senteflo))
        return G
if __name__ == '__main__':
    G = nx.Graph()
    ranking = rank()
    ranking.Addnode('test.txt', G)
    ranking.Addedge(G, 0.01)
    G_pagerank = pagerank(G)
    # Find out the most important sentences
    keyphrase = sorted(G_pagerank, key=G_pagerank.get, reverse=True)
    print(keyphrase[0],keyphrase[1],keyphrase[2])

        




        
    


