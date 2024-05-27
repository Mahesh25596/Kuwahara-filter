#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2


# In[9]:


class Adaptive_kuwahara:
    def cal_mean(self, img, x,y,window):
        r = int((window/2)+1)
        means=[0,0,0,0]
        means[0] = int(np.mean(img[x-r+1:x+1, y-r+1:y+1]))
        means[1] = int(np.mean(img[x-r+1:x+1, y:y+r]))
        means[2] = int(np.mean(img[x:x+r, y-r+1:y+1]))
        means[3] = int(np.mean(img[x:x+r, y:y+r]))
        return means
    def cal_var(self, img, x,y,r):
        var=[0.0,0.0,0.0,0.0]
        var[0] = np.var(img[x-r+1:x+1, y-r+1:y+1])
        var[1] = np.var(img[x-r+1:x+1, y:y+r])
        var[2] = np.var(img[x:x+r, y-r+1:y+1])
        var[3] = np.var(img[x:x+r, y:y+r])
        return var
    def replace_value(self, v,s,h, x, y, value1,value2,value3):
        v[x,y]= value1
        s[x,y]= value2
        h[x,y]= value3
        return h,s,v
    def feasibility(self, x,y,r,v):
        rows,cols = v.shape
        if (((x-r+1)>=0) and ((y-r+1)>=0) and ((x+r)<rows) and ((y+r)<cols)):
            return True
        else:
            return False
    def adapt_var(self, v, temp, x, y):
        best_window = temp
        best_var = [0.0,0.0,0.0,0.0]
        temp_var = [0.0,0.0,0.0,0.0]
        for i in range(9):
            r = int((temp/2)+1)
            if self.feasibility(x,y,r,v):
                temp_var = self.cal_var( v, x,y,r)
                if all(v == 0 for v in best_var):
                    best_var = temp_var
                elif min(best_var)>min(temp_var):
                    best_var = temp_var
                    best_window = temp
        return best_var,best_window
    def Adapted_kuwahara_filter (self, img, window):
        r = int((window/2)+1)
        best_window = window
        h, s, v = cv2.split(img)
        rows, cols = v.shape
        for x in range(r-1, rows-r):
            for y in range (r-1, cols-r):

                    mean1= [0,0,0,0]
                    mean2= [0,0,0,0]
                    mean3= [0,0,0,0]
                    var=[0.0,0.0,0.0,0.0]
                    var, best_window = self.adapt_var(v, window, x, y)
                    mean1 = self.cal_mean( v,x,y,window)
                    mean2 = self.cal_mean( s,x,y,window)
                    mean3 = self.cal_mean(h,x,y,window)
                    h,s,v = self.replace_value( v,s,h,x,y,mean1[var.index(min(var))],mean2[var.index(min(var))],mean3[var.index(min(var))])
        return cv2.merge([h,s,v])


# In[10]:


img1 = cv2.imread(r"C:\Users\mahes\OneDrive\Desktop\Gray S&P.jpg")
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)


process = Adaptive_kuwahara()
img1 = process.Adapted_kuwahara_filter ( img1, 3)

brightened_img = cv2.cvtColor(img1, cv2.COLOR_HSV2BGR)
#cv2.imshow(brightened_img)
#cv2.imshow('Example Image', brightened_img)

#cv2.imwrite(r"C:\Users\mahes\OneDrive\Desktop\k.jpg", brightened_img)
plt.imshow(brightened_img)
#cv2.imwrite(r"C:\Users\mahes\OneDrive\Desktop\grey_k.jpg", image_k)


# In[27]:


cv2.imwrite(r"C:\Users\mahes\OneDrive\Desktop\Gray_S&P_AK_9.jpg", brightened_img)


# In[16]:


cv2.imwrite("C:\\Users\\mahes\\OneDrive\\Desktop\\A_k1.jpg", brightened_img)


# In[ ]:




