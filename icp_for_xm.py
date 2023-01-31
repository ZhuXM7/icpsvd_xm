import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import time

def ICPSVD(source, target, threshold, maxIteration, pltornot):
    print(8)
    source_mod, source_centroid = shift_model_to_origin(source)
    target_mod, target_centroid = shift_model_to_origin(target)
    print(6)

    finhom = np.identity(4)
    reqR = np.identity(3)
    reqT = [0.0, 0.0, 0.0]
    TREE = KDTree(target_mod)
    print(7)
    n = np.size(source_mod, 0)
    print(9)
    err = 999999
    errStorage = []
    print(10)


    for i in range(maxIteration):
        start_time = time.time()
        preverr = err
        """Conduct a tree search"""
        # print(type(source_mod), source_mod)
        print(11)
        distance, index = TREE.query(source_mod)
        print(1)
        # print(distance, index)
        index_list = index.tolist()
        # print(len(source_mod), len(target_mod))

        # [print(target_name_list[i][0],source_name_list[index_list[i]][0]) for i in range(len(target))]

        """Calculate and store the Error"""
        err = np.sqrt(np.mean(distance ** 2))
        errStorage.append(err)
        print(2)

        """Calculate the Centroid of moving and fixed point clouds (Corresponded points)"""
        com = np.mean(source_mod, 0)
        cof = indxtMean(index, target_mod)
        print(3)
        """Form the W matrix to calculate the necessary Rot Matrix"""
        W = np.dot(np.transpose(source_mod), indxtfixed(index, target_mod)) - n * np.outer(com, cof)
        U, _, V = np.linalg.svd(W, full_matrices=False)
        tempR = np.dot(V.T, U.T)
        print(4)
        """Calculate the Needed Translation"""
        tempT = cof - np.dot(tempR, com)
        print(5)
        """Apply the Computed Rotation and Translation to the Moving Points"""
        source_mod = (tempR.dot(source_mod.T)).T
        source_mod = np.add(source_mod, tempT)
        print(6)
        """Store the RotoTranslation"""
        reqR = np.dot(tempR, reqR)
        reqT = np.add(np.dot(tempR, reqT), tempT)
        print('{} Cycle the MSE is equal to {}'.format(i + 1, err))
        if pltornot == True:
            plotter(target_mod, source_mod, i)
            """Error Check """
        if abs(preverr - err) < threshold:
            """Create a Homogeneous Matrix of the Results and plot"""
            finhom[0:3, 0:3] = reqR[0:, 0:]
            finhom[0:3, 3] = reqT[:]
            print(distance, index)
            print('\nThe Algorithm has exited on the {}th iteration with Error: {}\n'.format(i + 1, err))
            print('The Homogeneous Transformation matrix =\n \n {}'.format(finhom))
            break
        end_time = time.time()
        print("Takes: {:.2f}秒".format(end_time - start_time))

    return finhom, errStorage, source_mod

def shift_model_to_origin(node_array):
    # print("before", node_array[len(node_array)-1])
    centroid = np.mean(node_array, axis=0)
    node_array = node_array - centroid
    # print("centroid", centroid)
    # print("after", node_array[len(node_array)-1])
    # print("length",len(node_array))
    # print("------------")

    return node_array, centroid

def indxtfixed(index, arrays):
    T = []
    for i in index:
        T.append(arrays[i])
    return np.asanyarray(T)

def plotter(fixed, moving, i):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(fixed[0:, 0], fixed[0:, 1], fixed[0:, 2], c='r', marker='o')
    ax.scatter(moving[0:, 0], moving[0:, 1], moving[0:, 2], c='b', marker='^')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    filename = str(i) + 'plot.png'
    fig.savefig(filename)
    plt.close(fig)
    return

def indxtMean(index, arrays):
    indxSum = np.array([0.0, 0.0, 0.0])
    for i in range(np.size(index, 0)):
        indxSum = np.add(indxSum, np.array(arrays[index[i]]), out=indxSum, casting='unsafe')
    return indxSum / np.size(index, 0)