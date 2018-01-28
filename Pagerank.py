import networkx as nx

def pagerank(G, max_iter = 100, damping = 0.85, weight = 'weight', tol = 1e-6):
    '''
    Calculate node's importance in G according node's degree and edge's weight
    
    :param G: 需要执行pagerank算法的图，执行pagerank算法之后，该图并不改变。
    :param max_iter: 最大迭代次数，默认为100次
    :param damping: 阻尼系数，默认为0.85
    :param weight: 图中边的权，默认为原图中边的权值
    :param tol: 允许的误差限度，默认为1e-6
    :return: 一个键为节点，值为节点权重的字典
    '''
    if len(G) is 0:
        return {}
    # Change G to directed because stochastic_graph function deal with directed graph
    if not G.is_directed():
        g = G.to_directed()
    else:
        g = G
    # copy the origin graph
    gcopy = nx.stochastic_graph(g, weight=weight)
    N = gcopy.number_of_nodes()
    x = dict.fromkeys(gcopy, 1/N)
    p = dict.fromkeys(gcopy, 1/N)
    dangling_weights = p
    # dangling_nodes is the node that outdegree is zero
    dangling_nodes = [n for n in gcopy if gcopy.out_degree(n, weight=weight) == 0.0]
    for _ in range(max_iter):
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        # find out all dangling_node
        danglesum = damping * sum(xlast[n] for n in dangling_nodes)
        for n in x:
            for nbr in gcopy[n]:
                # doing a left multiply
                x[nbr] += damping * xlast[n] * gcopy[n][nbr][weight]
            x[n] += danglesum * dangling_weights.get(n,0) + (1.0 - damping) * p.get(n,0)
    # check convergence
        Errorrate = sum([abs(x[n] - xlast[n]) for n in x])
        if Errorrate < N*tol:
            return x
    raise ValueError('The graph is not convergence')