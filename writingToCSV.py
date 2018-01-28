import fileWriter as c

#This writes data (key features of my image to a file dir path specified here. 
def writeToFile():
    file = open("myData.csv", "a",newline='')
    f = c.writeToFile("C:/Users/Zoe Tagboto/Documents/Fall 2017/Robotics Class/Final Project/Tensor Flow Edition/Images/test",100,100,file)
    f.buildFile()
    file.close()
    
writeToFile()
