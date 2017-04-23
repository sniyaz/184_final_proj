import pdb

import collada
import numpy as np
import sys


def extract_mesh_points(mesh_filename):
    mesh_data = open(mesh_filename, "rb+")
    mesh = collada.Collada(mesh_data)
    triangles = [i for i in mesh.geometries[0].primitives[0]]

    vertex_set = set()
    for tri in triangles:
        for vert in tri.vertices:
            vert_tup = tuple(vert)
            vertex_set.add(vert_tup)
 
    vertex_list = [np.array(v) for v in vertex_set]
    centroid = sum(vertex_list)
    centroid = centroid/len(vertex_list)
    #Hack to estimate each normal as pointing outward from center.
    normal_dict = {tuple(v) : v - centroid for v in vertex_list}

    return vertex_list, normal_dict 


