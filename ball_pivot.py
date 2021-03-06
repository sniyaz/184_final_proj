import pdb

import collada
import numpy as np
import sys
import random
from sklearn.neighbors import KDTree
from util import extract_mesh_points, trilaterate


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


def pivot(point_1, point_2, ball_center, ball_radius, kd_tree):
    """
    Takes the edge points pivoted around as well as the ball, and return the first
    point hit by pivoting the ball!
    """
    mid_point = (point_1 + point_2)/2
    trajectory_vec = ball_radius - mid_point
    trajectory_radius = np.linalg.norm(trajectory_vec)
    #TODO


def get_triangle_ball(p1, p2, p3, normal_dict, ball_radius):
    """
    Returns center of ball of given radius that touches all three points given.
    Note: Uses intersection of three spheres.
    """
    tri_normal = np.cross(p2 - p1, p3 - p1)
    tri_normal = tri_normal/np.linalg.norm(tri_normal)
    #Normal vec orientation check.
    if np.dot(tri_normal, normal_dict[tuple(p1)]) < 0:
        tri_normal = -tri_normal
    
    intersect_1, intersect_2 = trilaterate(p1, p2, p3, ball_radius, ball_radius, ball_radius)
    
    found_center = intersect_1
    if np.dot(tri_normal, found_center - p1) < 0:
        found_center = intersect_2
    
    return found_center


if __name__ == "__main__":

    mesh_filename = sys.argv[1]
    vertex_list, normal_dict = extract_mesh_points(mesh_filename)
    #TODO: Move this as a command line argument!
    radius = 2.0
    kd_tree = KDTree(np.array(vertex_list))
    
    seed_set = get_seed_set(vertex_list, normal_dict, kd_tree)
    
    get_triangle_ball(seed_set[0], seed_set[1], seed_set[2], normal_dict, radius)



