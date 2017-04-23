import pdb

import collada
import numpy as np
import sys


if __name__ == "__main__":

    mesh_name = sys.argv[1]
    mesh_data = open(mesh_name, "rb+")
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
    normal_list = [v - centroid for v in vertex_list] 

    pdb.set_trace()
    


