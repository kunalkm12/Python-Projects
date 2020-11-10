###############
##Design the function "findRotMat" to  return 
# 1) rotMat1: a 2D numpy array which indicates the rotation matrix from xyz to XYZ 
# 2) rotMat2: a 2D numpy array which indicates the rotation matrix from XYZ to xyz 
###############

import numpy as np
import cv2

def findRotMat(alpha, beta, gamma):
    ### xyz to XYZ
    r1 = np.array([[np.cos(np.deg2rad(alpha)), -1*np.sin(np.deg2rad(alpha)), 0],
                  [np.sin(np.deg2rad(alpha)), np.cos(np.deg2rad(alpha)), 0],
                  [0, 0, 1]])
    r2 = np.array([[1, 0, 0],
                  [0, np.cos(np.deg2rad(beta)), -1*np.sin(np.deg2rad(beta))],
                  [0, np.sin(np.deg2rad(beta)), np.cos(np.deg2rad(beta))]])
    r3 = np.array([[np.cos(np.deg2rad(gamma)), -1*np.sin(np.deg2rad(gamma)), 0],
                  [np.sin(np.deg2rad(gamma)), np.cos(np.deg2rad(gamma)), 0],
                  [0, 0, 1]])
    rotMat1 = np.matmul(r3,r2)
    rotMat1 = np.matmul(rotMat1,r1)
    
    ### XYZ to xyz
    grev = gamma*-1
    brev = beta*-1
    arev = alpha*-1
    r1 = np.array([[np.cos(np.deg2rad(grev)), -1*np.sin(np.deg2rad(grev)), 0],
                  [np.sin(np.deg2rad(grev)), np.cos(np.deg2rad(grev)), 0],
                  [0, 0, 1]])
    r2 = np.array([[1, 0, 0],
                  [0, np.cos(np.deg2rad(brev)), -1*np.sin(np.deg2rad(brev))],
                  [0, np.sin(np.deg2rad(brev)), np.cos(np.deg2rad(brev))]])
    r3 = np.array([[np.cos(np.deg2rad(arev)), -1*np.sin(np.deg2rad(arev)), 0],
                  [np.sin(np.deg2rad(arev)), np.cos(np.deg2rad(arev)), 0],
                  [0, 0, 1]])
    rotMat2 = np.matmul(r3,r2)
    rotMat2 = np.matmul(rotMat2,r1)
    return rotMat1, rotMat2


if __name__ == "__main__":
    alpha = 45
    beta = 30
    gamma = 50
    rotMat1, rotMat2 = findRotMat(alpha, beta, gamma)