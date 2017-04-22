import pdb

import collada
import sys


if __name__ == "__main__":

    mesh_name = sys.argv[1]
    mesh_data = open(mesh_name, "rb+")
    mesh = collada.Collada(mesh_data)
    triangles = [i for i in mesh.geometries[0].primitives[0]]


    pdb.set_trace()



