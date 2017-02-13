from snap import *
import random
import numpy as np
import sys
np.set_printoptions(threshold=np.nan)



def analyze_adjacent_matrix(m):
    edges = np.count_nonzero(m) / 2
    return edges

# return the analytical value of triangles
def number_of_triangles_real(m):
    m_3= np.dot(np.dot(m,m),m)
    return (np.trace(m_3)/6)

# def number_of_triangles(node_hash, target_id):
#     first_level_list = node_hash[target_id]
#     triangle_count = {}
#     for node_id in first_level_list:
#         second_level_list = node_hash[node_id]
#         triangle_count[node_id] = 1
#         for mid_id in second_level_list:
#             third_level_list = node_hash[mid_id]
#             for term_id in third_level_list:
#                 if (term_id == target_id):
#                     triangle_count[node_id] += 1
#     return triangle_count

def number_of_triangles(node_hash, target_id):
    first_level_list = node_hash[target_id]
    triangle_count = {}
    for node_id in first_level_list:
        second_level_list = node_hash[node_id]
        # triangle_count[node_id] = 1
        triangle_count[node_id] = len(list(set(first_level_list).intersection(second_level_list))) +1
    return triangle_count

def count_tu(u, node_hash):
    u_list = node_hash[u]
    u_list_tmp = node_hash[u]
    tu = 0
    for v in u_list:
        u_list_tmp.pop(0)
        for n in u_list_tmp:
            if (is_a_triangle(v,n,node_hash)):
                tu += 1
    return tu
def is_a_triangle(v ,n, node_hash):
    return (v in node_hash[n])


def random_walk_triagnels(node_hash, m, n = 30):
    PRESET_INITIAL = 0
    # pick a starting point
    if (PRESET_INITIAL == 0):
        u = random.randint(1,n)
        u_tri_status = number_of_triangles(node_hash, u)
        w_u = sum(u_tri_status.values())
        # t_u = count_tu(u, node_hash)
        # t_u = sum(u_tri_status.values())
        set_nodes = []
        du = len(u_tri_status.values())
    K = 10000
    Zk = []
    for i in range(0,K):
        v = u
        dv = du
        v_tri_status = u_tri_status
        step = 0
        flag = 1
        while (flag == 1):
            v = pick_based_on_triangles(v_tri_status, v)
            # print(70*'-')
            # print("node hash")
            # print(node_hash)
            # print(70*'-')
            # print('targeting node:{}'.format(v))
            # print(70*'-')
            v_tri_status = number_of_triangles(node_hash, v)
            # print(v_tri_status)
            # sys.exit()
            step += 1
            if (u == v):
                flag = 0
        Zk.append(step)
    # print("sum:{}".format(sum(Zk)/ float(6*len(Zk))))
    # print("du:{}, t_u is {}".format(du,t_u))
    # estimate_tri = sum(Zk) * (du + 2*t_u) / float(6*len(Zk)) - m/float(3)
    est_tri_list = []
    for i in range(0, len(Zk)):
        est_tri_list.append(sum(Zk[:i+1]) * du / float(2*len(Zk[:i+1])))
    write_to_txt(est_tri_list, 'random_walk_tri.txt')
    estimate_tri = sum(Zk) * (w_u) / float(6*len(Zk)) - m/float(3)
    return estimate_tri


def pick_based_on_triangles(triangle_dict, v_id):
    triangle_list = triangle_dict.values()
    random_val = random.random()
    rsum = 0
    res = 0
    total_degree = 0
    prob_list = []
    total = sum(triangle_list)
    prob_list = [x / float(total) for x in triangle_list]
    for prob in prob_list:
        rsum += prob
        if (random_val < rsum):
            return triangle_dict.keys()[res]
        res += 1

def random_walk_edges(m, node_hash, n = 60):
    u = random.randint(1,n)
    u_connection = node_hash[u]
    du = len(u_connection)

    p = random.randint(1,n)
    while (u == p):
        p = random.randint(1,n)

    K = 10000 # number of traversals
    Zk = []
    fx = []
    for i in range(0,K):
        v = u
        dv = du
        v_connection = u_connection
        step = 0
        flag = 1
        fx_count = 0
        while (flag == 1):
            v = v_connection[random.randint(0,dv-1)]
            v_connection = node_hash[v]
            dv = len(v_connection)
            step += 1
            if (p == v):
                fx_count += 1
            if (u == v):
                flag = 0
        Zk.append(step)
        fx.append(fx_count)
    # m = Z(k)d(u) / 2k
    # estimated_m_regenerative = sum(fx)/(len(fx)) * du
    estimated_m = sum(Zk) * du / float(2*len(Zk))
    est_m_list = []
    for i in range(0, len(Zk)):
        est_m_list.append(sum(Zk[:i+1]) * du / float(2*len(Zk[:i+1])))
    write_to_txt(est_m_list, 'random_walk_edges.txt')
    return estimated_m

def write_to_txt(m, file_name):
    with open(file_name, 'w') as f:
        for item in m:
            f.write("%s\n"%item)

def pick_for_counting_nodes(node_hash, v_id):
    v_connected = node_hash[v_id]
    dv = len(v_connected)
    # edge weight is now 1/u + 1/v
    edge_weights = [(1/float(dv) + 1/float(len(node_hash[node_id]))) for node_id in v_connected]
    prob_list = []
    total = sum(edge_weights)
    prob_list = [x / float(total) for x in edge_weights]
    index = 0
    rsum= 0
    random_val = random.random()
    for prob in prob_list:
        rsum += prob
        if (random_val < rsum):
            return v_connected[index]
        index += 1



def random_walk_nodes(node_hash,n = 60):
    u = random.randint(1,n)
    u_connection = node_hash[u]
    du = len(u_connection)
    u_edge_weights = [(1/float(du) + 1/float(len(node_hash[node_id]))) for node_id in u_connection]
    wu = sum(u_edge_weights)

    K = 10000
    Zk = []
    for i in range (0,K):
        v = u
        v_connection = u_connection
        step = 0
        flag = 1
        while (flag == 1):
            v = pick_for_counting_nodes(node_hash, v)
            step += 1
            if (u == v):
                flag = 0
        Zk.append(step)
    # m = Z(k)d(u) / 2k
    est_n_list = []
    for i in range(0, len(Zk)):
        est_n_list.append(sum(Zk[:i+1]) * wu / float(2*len(Zk[:i+1])))
    write_to_txt(est_n_list, 'random_walk_nodes.txt')
    estimated_nodes = sum(Zk)*wu / (2*K)
    return estimated_nodes

# def random_walk_nodes_cycle(node_hash, n = 60):
#     u = random.randint(1,n)
#     u_connection = node_hash[u]
#     du = len(u_connection)
#
#     p = random.randint(1,n)
#     while (u == p):
#         p = random.randint(1,n)
#
#     K = 10000 # number of traversals
#     fx = []
#     fx_count = 0
#     for i in range(0,K):
#         v = u
#         dv = du
#         v_connection = u_connection
#         step = 0
#         flag = 1
#         fx_count = 0
#         while (flag == 1):
#             v = v_connection[random.randint(0,dv-1)]
#             v_connection = node_hash[v]
#             dv = len(v_connection)
#             fx_count += 1/float(dv)
#             if (u == v):
#                 flag = 0
#         fx.append(fx_count)
#     # m = Z(k)d(u) / 2k
#     # print(fx)
#     # print(du)
#     estimated_m_regenerative = sum(fx)/(len(fx)) * du
#     return estimated_m_regenerative
#
# def random_walk_cfrp_edges(node_hash, n = 60):
#     u = random.randint(1,n)
#     v = random.randint(1,n)
#     while (u == v):
#         v = random.randint(1,n)
#     u_connection = node_hash[u]
#     du = len(u_connection)
