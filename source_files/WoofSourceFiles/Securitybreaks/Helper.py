import os

class Helper():
    def findFile_Read(self,name, path):
        filePath=""
        for root, dirs, files in os.walk(os.getcwd()):
            if name in files:
                return open(os.path.join(root, name),"r")
        return open(path+"\\"+name,"a") 
    
    def findFile_Write(self,name, path):
        filePath=""
        for root, dirs, files in os.walk(os.getcwd()):
            if name in files:
                return open(os.path.join(root, name),"a")
        return open(path+"\\"+name,"w")  
    