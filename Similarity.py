import math
from jieba import cut

def simi(sente1, sente2):
    '''
    Demo
     Judge the Similarity of two different sentences
    '''
    count = 0
    seq1 = list(cut(sente1))
    seq2 = list(cut(sente2))
    ''' for word1 in seq1:
        for word2 in seq2:
            if word1 == word2:
                count = count + 1
    '''
    count = len(set(seq1) & set(seq2))
    return count/(math.log10(len(seq1)) + math.log10(len(seq2)))



