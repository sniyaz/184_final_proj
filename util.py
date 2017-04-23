import pdb

import collada
import numpy as np
import sys

from numpy import sqrt, dot, cross                       
from numpy.linalg import norm     

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


def trilaterate(P1,P2,P3,r1,r2,r3):
    """
    Find intersection of three spheres. 
    Credit: http://stackoverflow.com/questions/1406375/finding-intersection-points-between-3-spheres
    """
    temp1 = P2-P1                                        
    e_x = temp1/norm(temp1)                              
    temp2 = P3-P1                                        
    i = dot(e_x,temp2)                                   
    temp3 = temp2 - i*e_x                                
    e_y = temp3/norm(temp3)                              
    e_z = cross(e_x,e_y)                                 
    d = norm(P2-P1)                                      
    j = dot(e_y,temp2)                                   
    x = (r1*r1 - r2*r2 + d*d) / (2*d)                    
    y = (r1*r1 - r3*r3 -2*i*x + i*i + j*j) / (2*j)       
    temp4 = r1*r1 - x*x - y*y                            
    if temp4<0:                                          
        raise Exception("The three spheres do not intersect!");
    z = sqrt(temp4)                                      
    p_12_a = P1 + x*e_x + y*e_y + z*e_z                  
    p_12_b = P1 + x*e_x + y*e_y - z*e_z                  
    return p_12_a,p_12_b 




