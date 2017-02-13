from hybrid_triangle_closing_model import *
# hybrid_triangle returns a adjacent matrix
# hybrid_triangle_with_Graph returns a proper graph
from random_walk import *
from cycle_formula import *
import pickle

def main():
    n = 100
    CREATE_GRAPH = 0
    EDGES = 1
    TRIANGLE = 1
    NODES = 1
    SAVE_MODEL = 1
    LOAD_MODEL = 0

    node_hash = {
        1: [2,3],
        2: [1,3],
        3: [1,2]
    }
    if (SAVE_MODEL == 1):
        m = hybrid_triangle(node_hash, n)
        with open("hybrid_triangle_model.pkl","wb") as f:
            pickle.dump(m, f)
    if (LOAD_MODEL == 1):
        with open("hybrid_triangle_model.pkl", "rb") as f:
            m = pickle.load(f)
        # print(m)
    if (EDGES):
        edges = analyze_adjacent_matrix(m)
        estimated_edges= random_walk_edges(m, node_hash, n)
        print("Number of edges of the graph is {}".format(edges))
        print("Number of estimted edges of the graph is {}".format(estimated_edges))
        if (CREATE_GRAPH == 1):
            DrawGViz(G, gvlDot, "network.png"," ", True)
    if (TRIANGLE):
        # print(m)
        tri =  number_of_triangles_real(m)
        tri_est = random_walk_triagnels(node_hash,edges, n)
        print("Number of estimated triangles is {}".format(tri_est))
        # tri_cycle = random_walk_triagnels_cycle(node_hash, n)
        # print("Number of estimated triangles from cycle is {}".format(tri_cycle))
        print("Number of triangles is {}".format(tri))
    if (NODES):
        nodes_est = random_walk_nodes(node_hash, n)
        nodes_est_cycle = random_walk_nodes_cycle(node_hash, n)
        print("Number of estimated nodes is {}".format(nodes_est))
        print("Number of estimated nodes by cycle formula is {}".format(nodes_est_cycle))
        print("Number of nodes is {}".format(n))

if __name__ == '__main__':
    main()
