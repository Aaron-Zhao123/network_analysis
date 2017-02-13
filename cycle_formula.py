# from snap import *
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

def number_of_triangles(node_hash, target_id):
    first_level_list = node_hash[target_id]
    triangle_count = {}
    for node_id in first_level_list:
        second_level_list = node_hash[node_id]
        # triangle_count[node_id] = 1
        triangle_count[node_id] = len(list(set(first_level_list).intersection(second_level_list))) +1
    return triangle_count


def count_tu(u, node_hash):
    u_list = node_hash[u][:]
    u_list_tmp = node_hash[u][:]
    tu = 0
    for x in u_list:
        u_list_tmp.remove(x)
        for n in u_list_tmp:
            if (is_a_triangle(x,n,node_hash)):
                tu += 1
    return tu
def count_tuv(u, v, node_hash):
    first_list = set(node_hash[u])
    second_list = set(node_hash[v])
    return len(first_list.intersection(second_list))

def is_a_triangle(v ,n, node_hash):
    return (v in node_hash[n])

def random_walk_triagnels_cycle(node_hash, n = 30):
    u = random.randint(1,n)
    u_connection = node_hash[u]
    du = len(u_connection)

    u_tri_status = number_of_triangles(node_hash, u)
    # wu_two = sum([number_of_triangles(node_hash, u, second) for second in u_connection])
    wu_two = sum(u_tri_status.values())
    tu = count_tu(u, node_hash)
    wu = 2*tu + du

    # print(node_hash)
    # print('couting:{}'.format(count_tuv(10,11,node_hash)))
    # sys.exit()

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
            tv = count_tu(v,node_hash)
            v = v_connection[random.randint(0,dv-1)]
            tuv = count_tuv(prev_v, v, node_hash)
            wv = 2*tv + dv
            # fx_count += (wv) / float(dv)
            fx_count += tv / float(wv)
            # fx_count += (tuv) / float(dv)
            v_connection = node_hash[v]
            dv = len(v_connection)
            # tuv = count_tuv(prev_v, v, node_hash)
            # tv = count_tu(v,node_hash)
            prev_v = v
            if (u == v):
                flag = 0
        fx.append(fx_count)
    # print(fx)
    print("Average is {}".format(sum(fx)/(len(fx))))
    print("du is {}, tu is {}, wu is {}".format(du, tu, wu))
    print("another wu is {}".format(wu_two))
    est = sum(fx)/(len(fx)) * du
    return est
