# Based on Y. Li, D. McLean, Z. A. Bandar, J. D. O'Shea and K. Crockett, "Sentence similarity based on semantic nets and corpus statistics," in IEEE Transactions on Knowledge and Data Engineering, vol. 18, no. 8, pp. 1138-1150, Aug. 2006. doi: 10.1109/TKDE.2006.130 URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1644735&isnumber=34468

from jieba import cut
import numpy as np

# significance of semantic similarity
delta = 0.8

# word similarity threshold
sigma = 0.5

syndict = {}
for l in open('wn-data-cmn.tab',encoding='utf8').readlines():
    if l[0] == '#':
        continue
    synset, cmn, wexp = l.strip().replace(' ', '').split()
    wf = ''
    for f in wexp.split('+'):
        wf += f
        syndict[wf] = synset

def simi(s1, s2):
    s1 = tuple(cut(s1))
    s2 = tuple(cut(s2))
    j = mkjoint(s1, s2)
    return delta * semsim(s1, s2, j) + (1. - delta) * ordsim(s1, s2, j)

def mkjoint(s1, s2):
    'Generate joint set'
    return tuple(set(s1).union(set(s2)))

def ordsim(s1, s2, j):
    'Word Order Similarity between Sentences'
    s1 = mkorder(s1, j)
    s2 = mkorder(s2, j)
    return 1. - np.linalg.norm(s1 - s2) / np.linalg.norm(s1 + s2)

def mkorder(s, j):
    'Generate word order vector'
    d = {}
    for i in range(len(s)):
        d[s[i]] = i + 1
    v = np.zeros(len(j))
    for i in range(len(j)):
        if j[i] in d:
            v[i] = d[j[i]]
        else:
            m = 0.
            for w in d:
                t = wordsim(w, j[i])
                if t > sigma and t > m:
                    m = t
                    v[i] = d[w]
    return v

def semsim(s1, s2, j):
    v1 = mkvec(s1, j)
    v2 = mkvec(s2, j)
    return np.sum(v1 * v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def mkvec(s, j):
    v = np.zeros(len(j))
    for i in range(len(j)):
        if j[i] in s:
            v[i] = 1.
        else:
            m = 0.
            for w in s:
                t = wordsim(w, j[i])
                if t > m:
                    m = t
            if m > sigma:
                v[i] = m
            else:
                v[i] = 0
    return v

def wordsim(w1, w2):
    'Semantic Similarity between Words'
    if w1 == w2:
        return 1.
    if w1 not in syndict or w2 not in syndict:
        return 0.
    if syndict[w1] == syndict[w2]:
        return 0.9
    return 0.

if __name__ == '__main__':
    print('Enter 1: ', end='')
    s1 = input()
    print('Enter 2: ', end='')
    s2 = input()
    print(simi(s1, s2))
