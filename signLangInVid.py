import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

def contourCount(myDict):
    for key in myDict:
       if myDict[key] == max(myDict.values()):
           return key

#This is the color of the glove I want to find. Set for blue
def colToFind():
    lower_blue = np.array([70,70,100])
    upper_blue = np.array([180,180,250])
    return lower_blue, upper_blue


def main():

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()

        #blur = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #The color of my glove
        lower_col,upper_col = colToFind()
        

        #Makes everything except anything that is the same color
        #as my glove black 
        mask = cv2.inRange(hsv, lower_col, upper_col)
        res = cv2.bitwise_and(frame,frame, mask= mask)

        kernel = np.ones((5,5), np.uint8)

        #This is to reduce the noise in the background
        erosion = cv2.erode(mask, kernel, iterations = 1)
        dilation = cv2.dilate(mask, kernel, iterations = 1)
        

        #I want to find the extreme contours of my hand.
        image,contours, hierachy = cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cList={}
        for i in range(len(contours)):
            cList[i]=len(contours[i])
        
        try:
            cnt = contours[contourCount(cList)]
            hull = cv2.convexHull(cnt, returnPoints = False)

            #defects returns an array with start,end,farthest point,distanceToFarthest point
            #use cosine rule to find anfle for all defects
            defects = cv2.convexityDefects(cnt,hull)
            countDefects =0
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                cv2.line(frame,start,end,[0,255,0],2)
                cv2.circle(frame,far,5,[0,0,255],-1)

                #Got this idea from Hand Gesture Recognition Using Webcam (Published Paper)
                #length of triangle sides
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

                # cosine rule to get angle. This helps me determine
                # how many fingers are being held up
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

                if angle<=90:
                    countDefects +=1

            #Based on the number of fingers I can identify which signs the user
                    #is doing. I then print out on the frame
            if countDefects ==1:
                cv2.putText(frame,"This is: C",(40,40),cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            elif countDefects == 2:
                cv2.putText(frame, "This is: I Love you", (40,40), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            elif countDefects == 3:
                cv2.putText(frame,"This is: B", (40,40), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            elif countDefects == 4:
                cv2.putText(frame,"This is: Five", (40,40), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            else:
                cv2.putText(frame,"This is: D", (40,40),cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        
        except:
            pass

        #Displays the normal frame
        cv2.imshow('frame',frame)

        #displays the frame with mask applied
        cv2.imshow('res',res)
        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
             break

    cv2.destroyAllWindows()
    cap.release()

main()

 
