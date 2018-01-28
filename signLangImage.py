import cv2
import numpy as np
import pandas as pd

#This picks the largest contour value. 90% of the time its the hand
def contourCount(myDict):
    for key in myDict:
       if myDict[key] == max(myDict.values()):
           return key

#This function matches an image to a template 
def recognise(img, lookingFor):

    img_rgb = cv2.imread(img)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(lookingFor,0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)

    cv2.imshow('Detected',img_rgb)
#recognise('blueB.jpg','bluerA.jpg')


#This is for image processing to extract main points.     
def recognize(img):
    img = cv2.imread(img,600)
    #Applies a blue to the image
    blur = cv2.fastNlMeansDenoisingColored(img,None,100,10,7,21)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    #The color of my glove
    lower_blue = np.array([40,70,160])
    upper_blue = np.array([250,250,250])

    #Makes everything except anything that is the same color
    #as my glove black 
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(blur,blur, mask= mask)

    kernel = np.ones((5,5), np.uint8)

    #This is to reduce more noise in the background

    dilation = cv2.dilate(mask, kernel, iterations = 1)
    

    #I want to find the extreme contours of my hand.
    image,contours, hierachy = cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #print("Contours")
    cList={}
    for i in range(len(contours)):
        cList[i]=len(contours[i])
        #print("Contour",i,"points:",len(contours[i]))


    # These are the steps I go through in order to get the key features
    # of my image 
    cv2.imshow('img',img)
    cv2.imshow('Det',blur)
    cv2.imshow('res', res)
    cv2.imshow('dilation',dilation)
        
        #This calculates the convex points (tips of fingers)
    #and the defects the deep points on the fingers which
    #should help me to understand how many fingers are
    #up
    try:
        cnt = contours[contourCount(cList)]

        hull = cv2.convexHull(cnt, returnPoints = True)
        #print("hull are",hull)
        return hull

        #defects returns an array with start,end,farthest point,distanceToFarthest point
        defects = cv2.convexityDefects(cnt,hull)
        #print("defects are",defects)
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            cv2.line(img,start,end,[0,255,0],2)
            cv2.circle(img,far,5,[0,0,255],-1)
            print(defects)
        

    except:
        pass

recognize("1_3.jpg")


    
