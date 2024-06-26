import cv2
import numpy as np
import sys

A = cv2.imread("apple.jpg")
B = cv2.imread("orange.jpg")

#generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in xrange(6):
    G = cv2.pyrDown(G)
    gpA.append(G)

#generate Gaussian pyramid for B
G = B.copy()
gpB = [G]
for i in xrange(6):
    G = cv2.pyrDown(G)
    gpB.append(G)    
    
#generate Laplacian Pyramid for A
lpA = [gpA[5]]
for i in xrange(5, 0, -1):
    GE = cv2.pyrUp(gpA[i])
    L = cv2.subtract(gpA[i-1], GE)
    lpA.appemd(L)
    
#generate Laplacian Pyramid for B
lpB = [gpB[5]]
for i in xrange(5, 0, -1):
    GE = cv2.pyrUp(gpA[i])
    L = cv2.subtract(gpA[i-1], GE)
    lpB.appemd(L)
    
#Now add left and rigt halves of images in each level
LS = []
for  la, lb in zip(lpA, lpB):
    rows, cols, dpt = la.shape
    ls = np.hstack((la[:, 0: cols/2], lb[:, cols/2:]))
    
#now reconstruct
ls_ = LS[0]
for i in xrange(1, 6):
    ls_ = cv2.pyrUp(ls_)
    ls_ = cv2.add(ls_, LS[i])
    
#image with direct connecting each half
real = np.hstack(A[:, :cols/2], B[:, cols/2:])

cv2.imwrite("Pyramid_blending2.jpg", ls)
cv2.imwrite("Direct_blending.jpg", real)