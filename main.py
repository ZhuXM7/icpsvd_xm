import numpy as np
from las import LASFILE
from icp_for_xm import ICPSVD
import laspy


las_base = laspy.read('digi v4 221215 base Export.las')
las_ran = laspy.read('digi v4  221215 Export.las')
array_base,array_ran = LASFILE(las_base,las_ran)
fixed=np.asarray(array_base)
moving=np.asarray(array_ran)
moving = moving-np.array([1.9, -4.4, 1.5])
# temp = []
# with open('point_cloud_a.txt') as f:
#     for l in f:
#             x, y, z = l.split()
#             temp.append([float(x), float(y), float(z)])
# fixed=np.asarray(temp)
# temp = []
# with open('point_cloud_b.txt') as f:
#     for l in f:
#             x, y, z = l.split()
#             temp.append([float(x), float(y), float(z)])
# moving=np.asarray(temp)
finhom, errStorage, source_mod=ICPSVD(fixed,moving,0.0001,100,True)
print(finhom,errStorage,source_mod)