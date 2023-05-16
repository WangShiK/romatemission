import numpy as np
import cv2
from osgeo import gdal
import math


data = gdal.Open("land_water_boundary_raster2022.tif")
geo = data.GetGeoTransform()
im = cv2.imread("land_water_boundary_raster2022.tif")
im = im * 255
img = cv2.imread("land_water_boundary_raster2022.tif", 0)
img = img * 255

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

dst = cv2.erode(img, kernel, iterations=3)



coutours, his = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



area = []
for k in range(len(coutours)):
    area.append(cv2.contourArea(coutours[k]))
max_idx = np.argmax(np.array(area))

pts = coutours[max_idx]
pts = np.int32(pts)

im_show = cv2.drawContours(im, [pts], 0, (0, 0, 255), 10)
length = cv2.arcLength(coutours[max_idx], True)
print(length)
#cv2.imwrite("draw123.tif", im_show)

pt = []
ulX = geo[0]
ulY = geo[3]
pixWidth = geo[1]
pixHeight = geo[5]
rotate1 = geo[2]
rotate2 = geo[4]

for i in range(len(pts)):
    p = pts[i].reshape(-1)
    Xgeo = ulX + p[0] * pixWidth + p[1] * rotate1
    Ygeo = ulY + p[0] * rotate2 + p[1] * pixHeight
    pt.append((Xgeo, Ygeo))

pt = np.array(pt)

from multiprocessing import Process
import xlrd
import xlwt  #对xls文件进行改写
from xlutils.copy import copy
#二维数组转excel储存


def transformation(ls2):
        #ls2为二维数组
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Sheet")

        for i in range(len(ls2)):
                for j in range(len(ls2[i])):
                        sheet.write(i, j, ls2[i][j])

        workbook.save("list2Excel.xls")

        
def get_len(pt):
    print(len(pt))
    l = 0
    for i in range(len(pt) - 100):
        if i == len(pt) - 1:
            l += np.sqrt(math.pow((pt[i][0] - pt[0][0]), 2) + math.pow((pt[i][1] - pt[0][1]), 2))
        l += np.sqrt(math.pow((pt[i + 1][0] - pt[i][0]), 2) + math.pow((pt[i + 1][1] - pt[i][1]), 2))

    return l
        
       



