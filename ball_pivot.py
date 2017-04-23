import pdb

import collada
import numpy as np
import sys
import random
from sklearn.neighbors import KDTree
from util import extract_mesh_points


def get_seed_set(vertex_list, normal_dict, kd_tree):
    """Cheap trick that we can probably do better than: pick a random point, then  
    find the two closest points. Test the three as a potential seed set.
    """
    while True:
        rand_vertex = random.choice(vertex_list)
        nearest_2 = kd_tree.query(rand_vertex, k=3, return_distance=False)[0][1:]
	
        first_neighbor = vertex_list[nearest_2[0]]
        second_neighbor = vertex_list[nearest_2[1]]
        seed_set = [rand_vertex, first_neighbor, second_neighbor] 

        if check_seed_set(seed_set, normal_dict):
            return seed_set


def check_seed_set(seed_set, normal_dict):
    tri_vec_1 = seed_set[1] - seed_set[0]
    tri_vec_2 = seed_set[2] - seed_set[0]
    tri_normal = np.cross(tri_vec_1, tri_vec_2)
    
    dot_prods = [np.dot(normal_dict[tuple(v)], tri_normal) for v in seed_set]
    test_vec = [d for d in dot_prods if d > 0]
    if len(test_vec) == 3:
        return True
    test_vec = [d for d in dot_prods if d < 0]
    if len(test_vec) == 3:
        return True
    
    return False

     
if __name__ == "__main__":

    mesh_filename = sys.argv[1]
    vertex_list, normal_dict = extract_mesh_points(mesh_filename)
    #TODO: Move this as a command line argument!
    radius = 1.0
    kd_tree = KDTree(np.array(vertex_list))
    
    seed_set = get_seed_set(vertex_list, normal_dict, kd_tree)
    
    pdb.set_trace()




