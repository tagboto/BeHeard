import signLangImage as t
import numpy as np
import cv2
import csv
from os import listdir
from os.path import isfile, join

class writeToFile:
  
    def __init__(self,path,height,width,file):
        if not path.endswith('/'):
            path = path + "/"
        self.path = path
        self.file = file
        self.height = height
        self.width = width
        self.type = type
        self.onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]

    #Before I process I shrink the file to make feature extraction better
    def prepareImage(self,pathx):
        path          = self.path + pathx
        img           = cv2.imread(path,600)
        img           = cv2.resize(img,(self.width,self.height), interpolation = cv2.INTER_CUBIC)
        img = np.reshape(img,(1,3,self.width,self.height))
        return (img)

    
    #I obtain the letter of file based on how I named the img.
    # E.g 10_3 is a C because it corresponds to the 3rd letter
    #of the alphabet
    def myLabel(self,file):
        dash          = file.rfind("_")
        dot           = file.rfind(".")
        classtype     = file[dash+1:dot]

        if classtype == '1':
            return 'A'

        elif classtype =='2':
            return 'B'

        elif classtype =='3':
            return 'C'

        elif classtype == '4':
            return 'D'

        elif classtype =='5':
            return 'E'

        elif classtype =='6':
            return 'F'

        elif classtype == '7':
            return 'G'

        elif classtype == '8':
            return 'H'

        elif classtype =='9':
            return 'I'

        else:
            return 'not found'

        
    #This gets the feature information for every image processed
    def buildFile(self):
        counter = 0
        chk = []
        comma = ","
        for file in self.onlyfiles:
            q = self.prepareImage(file)
            if (counter != 0):
                hull = t.recognize(file)
                flattenedHull = hull.flatten('F')
                label = self.myLabel(file)
                z = csv.writer(self.file,delimiter=',')
                z.writerow([file,label,flattenedHull])
                print("done",file,label))
            else:
                self.global_matrix = q
    
            counter = counter + 1

    
