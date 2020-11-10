"""
Image Stitching Problem
(Due date: Nov. 9, 11:59 P.M., 2020)
The goal of this task is to stitch two images of overlap into one image.
To this end, you need to find feature points of interest in one image, and then find
the corresponding ones in another image. After this, you can simply stitch the two images
by aligning the matched feature points.
For simplicity, the input two images are only clipped along the horizontal direction, which
means you only need to find the corresponding features in the same rows to achieve image stiching.

Do NOT modify the code provided to you.
You are allowed use APIs provided by numpy and opencv, except “cv2.findHomography()” and
APIs that have “stitch”, “Stitch”, “match” or “Match” in their names, e.g., “cv2.BFMatcher()” and
“cv2.Stitcher.create()”.
"""
import cv2
import numpy as np
import random

def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """
    img1 = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
    h1,w1,d1 = left_img.shape
    h2,w2,d2 = right_img.shape
    
    sift = cv2.SIFT_create()
    kp1, desc1 = sift.detectAndCompute(left_img, None)
    kp2, desc2 = sift.detectAndCompute(right_img, None) 
    matches = []
    for i, desc in enumerate(desc1):
        dif = np.sum(((desc2-desc)**2), axis = 1)
        bestInds = dif.argsort()[:2]
        match = (i, bestInds[0], dif[bestInds[0]] / dif[bestInds[1]])
        matches.append(match)
    
    src = np.float32([kp1[m[0]].pt for m in matches]).reshape(-1,1,2)
    dst = np.float32([kp2[m[1]].pt for m in matches]).reshape(-1,1,2)
    
    M, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    h1,w1 = img1.shape
    h2,w2 = img2.shape
    pts = np.float32([ [0,0],[0,h1-1],[w1-1,h1-1],[w1-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)
    img2 = cv2.polylines(img2, [np.int32(dst)], True, 255,3, cv2.LINE_AA)
    
    dst = cv2.warpPerspective(right_img, M, (w2+w1, h2))
    cv2.imshow('i', dst)    
    return dst

left_img = cv2.imread('left.jpg')
right_img = cv2.imread('right.jpg')
solution(left_img, right_img)

    

if __name__ == "__main__":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/task1_result.jpg',result_image)


