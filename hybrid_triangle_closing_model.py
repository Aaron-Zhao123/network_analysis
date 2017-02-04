from snap import *
import random
import numpy as np
import sys
np.set_printoptions(threshold=np.nan)



def preferential_attach_with_Graph(G):
    total_degree = 0
    prob_list = []
    random_val = random.random() #returns [0,1]
    rsum = 0
    res = 1
    for node in G.Nodes():
        info = (node, node.GetOutDeg())
        total_degree += node.GetOutDeg()
        prob_list.append(node.GetOutDeg())
    prob_list = [x / float(total_degree) for x in prob_list]
    for prob in prob_list:
        rsum += prob
        if (random_val < rsum):
            return res
        res += 1

def random_pick(node_hash, node_id):
    node_list = node_hash[node_id]
    return random.choice(node_list)

def adjacent_matrix(node_hash,n):
    m = np.zeros(n*n).reshape(n,n)
    for node_id in range(1, n+1):
        for item in node_hash[node_id]:
            m[node_id-1][item-1] = 1
    print('Is this adjacent matrix symmetric: {}'.format(
                                                (m.transpose() == m).all()))
    return m

def preferential_attach(node_hash, v_id):
    random_val = random.random()
    rsum = 0
    res = 1
    total_degree = 0
    prob_list = []
    for node_id in range(1,v_id):
        total_degree += len(node_hash[node_id])
        prob_list.append(len(node_hash[node_id]))
    prob_list = [x / float(total_degree) for x in prob_list]
    for prob in prob_list:
        rsum += prob
        if (random_val < rsum):
            return res
        res += 1

def hybrid_triangle(node_hash, n = 60):
    p = 0.6
    r = 3
    for v_id in range(4,n+1):
        # first attach to an existing vertex x chosen preferentially
        attach_list = []
        x_id = preferential_attach(node_hash, v_id)
        attach_list.append(x_id)

        # pick a random var and prob
        for i in range(0,(r-1)):
            random_val = random.random() #returns [0,1]
            if (random_val <= p):
                # with prob p, choose a node preferentially
                pick_x_id = preferential_attach(node_hash, v_id)
            else:
                # with prob 1-p, connect randomly to a neighbour of x
                pick_x_id = random_pick(node_hash, x_id)
            attach_list.append(pick_x_id)
        node_hash[v_id] = []
        for node_id in attach_list:
            node_hash[v_id].append(node_id)
            node_hash[node_id].append(v_id)
            # flush as a set, avoids duplicates
            node_hash[v_id] = list(set(node_hash[v_id]))
            node_hash[node_id] = list(set(node_hash[node_id]))
    m = adjacent_matrix(node_hash, n)
    return m


def hybrid_triangle_with_Graph(G, node_hash, n =60):
    p = 0.6
    # n = 600000
    r = 3
    for v_id in range(4,n+1):
        attach_list = []
        # first attach to an existing vertex x chosen preferentially
        x_id = preferential_attach_with_Graph(G)
        attach_list.append(x_id)


        # pick a random var and prob
        for i in range(0,(r-1)):
            random_val = random.random() #returns [0,1]
            if (random_val <= p):
                # with prob p, choose a node preferentially
                pick_x_id = preferential_attach_with_Graph(G)
            else:
                # with prob 1-p, connect randomly to a neighbour of x
                pick_x_id = random_pick(node_hash, x_id)
            attach_list.append(pick_x_id)
        G.AddNode(v_id)
        node_hash[v_id] = []
        for node_id in attach_list:
            G.AddEdge(v_id, node_id)
            node_hash[v_id].append(node_id)
            node_hash[node_id].append(v_id)
            # flush as a set, avoids duplicates
            node_hash[v_id] = list(set(node_hash[v_id]))
            node_hash[node_id] = list(set(node_hash[node_id]))
    # for node_id in range(1,n+1):
    #     print('node is {}, and attach list is {}'.format(node_id, node_hash[node_id]))
    m = adjacent_matrix(node_hash, n)
    # print(node_hash)
    # print(m)
    return G
