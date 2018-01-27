import networkx as nx

def pagerank(G, max_iter = 100, damping = 0.85, weight = 'weight', tol = 1e-6):
    '''
    Calculate node's importance in G according node's degree and edge's weight
    '''
    if len(G) is 0:
        return {}
    #Change G to directed because stochastic_graph function deal with directed graph
    if not G.is_directed():
        g = G.to_directed()
    else:
        g = G
    #copy the origin graph
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
        #find out all dangling_node
        danglesum = damping * sum(xlast[n] for n in dangling_nodes)
        for n in x:
            for nbr in gcopy[n]:
                #doing left multiply
                x[nbr] += damping * xlast[n] * gcopy[n][nbr][weight]
            x[n] += danglesum * dangling_weights.get(n,0) + (1.0 - damping) * p.get(n,0)
    # check convergence, l1 norm
        err = sum([abs(x[n] - xlast[n]) for n in x])
        if err < N*tol:
            return x
    raise ValueError('The graph is not convergence')