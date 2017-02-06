from snap import *
import random
import numpy as np
import sys
np.set_printoptions(threshold=np.nan)

def random_walk_nodes_cycle(node_hash, n = 30):
    u = random.randint(1,n)
    u_connection = node_hash[u]
    du = len(u_connection)

    p = random.randint(1,n)
    while (u == p):
        p = random.randint(1,n)

    K = 10000 # number of traversals
    fx = []
    fx_count = 0
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
            fx_count += 1/float(dv)
            if (u == v):
                flag = 0
        fx.append(fx_count)
    estimated_m_regenerative = sum(fx)/(len(fx)) * du
    return estimated_m_regenerative


#
# def number_of_triangles(node_hash, target_id, aim):
#     # print (node_hash)
#     first_level_list = node_hash[target_id]
#     total = 0
#     tri_cnt = 0
#     for node_id in first_level_list:
#         second_level_list = node_hash[node_id]
#         for term_id in second_level_list:
#             if (term_id == target_id):
#                 total += 1
#                 if (node_id == aim):
#                     tri_cnt += 1
#     return (tri_cnt/float(total))
#
def number_of_triangles(node_hash, target_id, second_target_id):
    first_level_list = node_hash[target_id]
    triangle_cnt = 0
    for node_id in first_level_list:
        if (node_id == second_target_id):
            triangle_cnt += 1
    return triangle_cnt

def random_walk_triagnels_cycle(node_hash, n = 30):
    u = random.randint(1,n)
    u_connection = node_hash[u]
    du = len(u_connection)
    wu = sum([number_of_triangles(node_hash, u, second) for second in u_connection])

    K = 10000 # number of traversals
    fx = []
    fx_count = 0
    for i in range(0,K):
        v = u
        dv = du
        v_connection = u_connection
        prev_v = v
        step = 0
        flag = 1
        fx_count = 0
        while (flag == 1):
            v = v_connection[random.randint(0,dv-1)]
            v_connection = node_hash[v]
            dv = len(v_connection)
            fx_count += number_of_triangles(node_hash, prev_v, v)
            prev_v = v
            if (u == v):
                flag = 0
        fx.append(fx_count)
    est = sum(fx)/(len(fx))
    return est
