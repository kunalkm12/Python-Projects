###############
##1. Design the function "rectify" to  return
# fundamentalMat: should be 3x3 numpy array to indicate fundamental matrix of two image coordinates. 
# Please check your fundamental matrix using "checkFunMat". The mean error should be less than 5e-4 to get full point.
##2. Design the function "draw_epilines" to  return
# draw1: should be numpy array of size [imgH, imgW, 3], drawing the specific point and the epipolar line of it on the left image; 
# draw2: should be numpy array of size [imgH, imgW, 3], drawing the specific point and the epipolar line of it on the right image.
# See the example of epilines on the PDF.
###############
from cv2 import imread, xfeatures2d, FlannBasedMatcher, cvtColor, COLOR_RGB2BGR, line, circle, computeCorrespondEpilines
import numpy as np
from matplotlib import pyplot as plt

def rectify(pts1, pts2):
    #...
    p1 = np.array(pts1)
    p2 = np.array(pts2)

    n = p1.shape[0]
    arr = np.ones((n,9))
    
    for i in range(n):
        x1 = p1[i,0]
        y1 = p1[i,1]
        x2 = p2[i,0]
        y2 = p2[i,1]
        arr[i] = [x1*x2, x1*y2, x1, y1*x2, y1*y2, y1, x2, y2, 1] 
    
    [u,s,v] = np.linalg.svd(np.matmul(np.transpose(arr),arr))
    f = v[-1].reshape(3,3)
    
    return f


def draw_epilines(img1, img2, pt1, pt2, fmat):
    #...
    p1 = np.array(pt1)
    p2 = np.array(pt2)
    l1 = computeCorrespondEpilines(p1.reshape(-1,1,2),1,fmat)
    l2 = computeCorrespondEpilines(p2.reshape(-1,1,2),1,fmat)
    print(l1)
    print("\n")
    print(l2)
    l1 = l1.reshape(-1,3)
    l2 = l2.reshape(-1,3)

    
    for i in l1:
        x0 = 0
        y0 = int((-1*i[2])/i[1])
        x1 = 1080
        y1 = int(-1*(i[2]+i[0]*1080)/i[1])
        img1 = line(img1, (x0,y0), (x1,y1), (220,20,60),5)

    for i in l2:
        x0 = 0
        y0 = int((-1*i[2])/i[1])
        x1 = 1080
        y1 = int(-1*(i[2]+i[0]*1080)/i[1])
        img2 = line(img2, (x0,y0), (x1,y1), (220,20,60),5)
    
    img1 = cvtColor(img1, COLOR_RGB2BGR)
    img2 = cvtColor(img2, COLOR_RGB2BGR)
    
    return img1, img2


def checkFunMat(pts1, pts2, fundMat):
    N = len(pts1)
    assert len(pts1)==len(pts2)
    errors = []
    for n in range(N):
        v1 = np.array([[pts1[n][0], pts1[n][1], 1]])#size(1,3)
        v2 = np.array([[pts2[n][0]], [pts2[n][1]], [1]])#size(3,1)
        error = np.abs((v1@fundMat@v2)[0][0])
        errors.append(error)
    error = sum(errors)/len(errors)
    return error
    
if __name__ == "__main__":
    img1 = imread('rect_left.jpeg') 
    img2 = imread('rect_right.jpeg')

    # find the keypoints and descriptors with SIFT
    sift = xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # FLANN parameters for points match
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)
    flann = FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    good = []
    pts1 = []
    pts2 = []
    dis_ratio = []
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.3*n.distance:
            good.append(m)
            dis_ratio.append(m.distance/n.distance)
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)
    min_idx = np.argmin(dis_ratio) 
    
    # calculate fundamental matrix and check error
    fundMat = rectify(pts1, pts2)
    error = checkFunMat(pts1, pts2, fundMat)
    print(error)
    
    # draw epipolar lines
    draw1, draw2 = draw_epilines(img1, img2, pts1[min_idx], pts2[min_idx], fundMat)
    
    # save images
    fig, ax = plt.subplots(1,2,dpi=200)
    ax=ax.flat
    ax[0].imshow(draw1)
    ax[1].imshow(draw2)
    fig.savefig('rect.png')