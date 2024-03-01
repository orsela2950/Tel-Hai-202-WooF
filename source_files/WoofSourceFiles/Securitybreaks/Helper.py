import os


class Helper:
    @staticmethod
    def findFile_Read(name, path):
        filePath = ""
        for root, dirs, files in os.walk(os.getcwd()):
            if name in files:
                return open(os.path.join(root, name), "r")
        return open(path + "\\" + name, "a")

    @staticmethod
    def findFile_Write(name, path):
        filePath = ""
        for root, dirs, files in os.walk(os.getcwd()):
            if name in files:
                return open(os.path.join(root, name), "a")
        return open(path + "\\" + name, "w")
