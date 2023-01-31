import numpy as np
import laspy

def LASFILE(las_base,las_ran):
    array_base = np.zeros([len(las_base.x),3])
    array_base[:,0]=las_base.x
    array_base[:,1]=las_base.y
    array_base[:,2]=las_base.z
    array_ran = np.zeros([len(las_ran.x), 3])
    array_ran[:, 0] = las_ran.x
    array_ran[:, 1] = las_ran.y
    array_ran[:, 2] = las_ran.z
    return array_base,array_ran

