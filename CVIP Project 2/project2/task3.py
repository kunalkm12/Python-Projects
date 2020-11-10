# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 22:16:48 2020

@author: Mary Sharmila Rongal
"""

import cv2
import numpy as np

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
    
#    src = np.zeros((len(matches), 2), dtype=np.float32)
#    dst = np.zeros((len(matches), 2), dtype=np.float32)
#    for i, match in enumerate(matches):
#        src[i, :] = kp1[match[0]].pt
#        dst[i, :] = kp2[match[1]].pt

    M, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    h1,w1 = img1.shape
    h2,w2 = img2.shape
    pts = np.float32([ [0,0],[0,h1-1],[w1-1,h1-1],[w1-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)
    img2 = cv2.polylines(img2, [np.int32(dst)], True, 255,3, cv2.LINE_AA)
    
    dst = cv2.warpPerspective(right_img, M, (w2+w1, h2))
    #dst[0:img2.shape[0], 0:img2.shape[1]] = right_img
    cv2.imshow('i', dst)    
    return dst

left_img = cv2.imread('left.jpg')
right_img = cv2.imread('right.jpg')
solution(left_img, right_img)

if __name__ == "_main_":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/task1_result.jpg',result_image)