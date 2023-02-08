import os
import os.path

import pyautocad as AC
from pyautocad import Autocad


class FileOperations:
    def __init__(self):
        self.point = [[],[]]
        self.counter = 0
        self.scansAll = []
        self.scanListSelect=[]
        self.scanPath = ""
        self.confirmation = bool
        self.saveAllAtOnce = bool
        self.scanlistSelect = []
        self.operation1 = ""
        self.operation2 = ""
        self.operationsSpecial = ""
        self.translationMatrix = ""
        self.translationMatrixPath = ""
        self.exForm = str
        self.currentDir = ""
        self.pathCC = "C:/Program Files/CloudCompare/"
    def getCloud(self):
        if len(self.scansAll) != 0:
            self.scansAll = []
        for lst in os.walk(self.scanPath):
            print(lst)
            for file in lst[2]:
                if file.endswith("ply") or file.endswith(".e57") or file.endswith(".bin") or file.endswith(".las") or file.endswith("zfs"):
                    self.scansAll.append(file)
    def nameCreator(self, recentCloud, suffix=""):
        name = str(recentCloud)
        name = name.split(".")
        name = name[0]
        name = name + suffix
        return name
    def baseDirCC(self):
        self.currentDir = os.getcwd()
        os.chdir(self.pathCC)

class CloudCompare(FileOperations):
            
    def __init__(self):
        FileOperations.__init__(self)
        self.prefix = ".\cloudcompare -AUTO_SAVE OFF"
        self.clearClouds = " -CLEAR"
    def printCommand(self, name):
        __path = self.scanPath
        __path += __path + "/" + name
        with open(__path, "w") as l:
            l.write(self.ccCommand)

    def clearAxis(self):
        self.point = [[],[]]
    def openCloud(self, cloud, globalShift):
        if self.operationsSpecial == "normals":
            command = " -COMPUTE_NORMALS -O " + globalShift + "\"" + cloud + "\""
        else:
            command = " -O " + globalShift + "\"" + cloud + "\""
        return command
    def translate(self):
        matrixParser = [[1,0,0],[0,1,0],[0,0,1],[0,0,0,1]]
        for i in range(3):
            matrixParser[i].append(self.translationMatrix[i])
            self.translationMatrixPath = self.scanPath + "/TranslationMatrix.txt"
        with open(self.translationMatrixPath, "w+") as f:
            matrix = ""
            for lst in matrixParser:
                row = ""
            for num in lst:
                row += str(num) + " "
            matrix += row + "\n"
        f.write(matrix)
        self.operation2 = " -APPLY_TRANS \"" + self.translationMatrixPath + "\""
    def orthofotoExport(self, resolution = 0.01, axis=2):
        self.operation1 = " -RASTERIZE -GRID_STEP "+ str(resolution) + " -VERT_DIR " + axis + " -OUTPUT_RASTER_RGB"
    def crop2DAutoCAD(self, cloud):
        acad = Autocad()
        self.saveAllAtOnce = True
        for obj in acad.iter_objects():
            coord = obj.coordinates
            i=2
            for coordinate in coord:
                if i%2 == 0:
                    self.point[0].append(coordinate)
                if i%2 == 1:
                    self.point[1].append(coordinate)
                i += 1
            self.counter += 1
        i = 0
        for v in range(int(self.counter)):
            if i>1:
                recent= int((i/4)+1)
            else:
                recent = 1
            print("square " + str(recent))
            points=""
            for n in range(4):
                points += str(self.point[0][i]) + " "
                points += str(self.point[1][i]) + " "
                i += 1
            self.ccCommand += " -O " + "\"" + cloud + "\"" + " -CROP2D Z 4 " + str(points)

    def recapPrep(self):
        i = 0
        cloudsPreped = []
        self.exForm = "e57"
        globalShift = "-GLOBAL_SHIFT AUTO "
        for cloud in self.scansAll:
            if i == 0:
                logName = FileOperations.nameCreator(cloud, suffix="_log.txt")
                cloudsNewE57= FileOperations.nameCreator(cloud, suffix=".e57")
                cloudsPreped.append(cloudsNewE57)
                cloud = self.scanPath + "/" + cloud
                self.ccCommand = self.prefix + self.openCloud(cloud, globalShift) + " -MERGE_CLOUDS -REMOVE_ALL_SFS" + self.operation1 + self.exportCloud(self.exForm, logName, timestamp=False) + self.clearClouds
                i += 1
            else:
                logName = FileOperations.nameCreator(cloud, suffix="_log.txt")
                cloudsNewE57= FileOperations.nameCreator(cloud, suffix=".e57")
                cloudsPreped.append(cloudsNewE57)
                cloud = self.scanPath + "/" + cloud
                self.ccCommand += self.openCloud(cloud, globalShift) + " -MERGE_CLOUDS -REMOVE_ALL_SFS" + self.operation1 + self.exportCloud(self.exForm, logName, timestamp=False) + self.clearClouds
                i += 1
        return cloudsPreped

    def recap(self,recapVar, recapName=""):
        if recapVar == False:
            i = 0
            for cloud in self.scansAll:
                cloud = self.scanPath + "/" + cloud
                if recapName == "":
                    name = cloud.split("/")
                    name = name[-1]
                    name = name.split(".")
                    name = name[0]
                    name = name.replace(" ","_")
                    recapBatch = FileOperations.nameCreator(self, cloud, suffix="_Recap.bat")

                elif recapName != "":
                    recapBatch = FileOperations.nameCreator(self, cloud, suffix="_Recap.bat")
                    name = recapName
                with open(recapBatch, "w+") as f:
                    batch = "\"C:/Program Files/Autodesk/Autodesk ReCap/Decap.exe\" --importWithLicense \"" + self.scanPath +"\" " + name + " \"" + cloud + "\""
                    f.write(batch)
        elif recapVar == True:
            if recapName == "":
                name = "RecapAlleDateien"
            recapBatch = self.scanPath + "/" + recapName + ".bat"
            recapIndices = self.scanPath + "/" + recapName + "_indices.txt" 
            recapCloudLst =  []
            for cloud in self.scansAll:
                cloud = self.scanPath + "/" + cloud
                recapCloudLst.append(cloud)
            with open(recapIndices, "w+") as rI:
                for entry in recapCloudLst:
                    entry += "\n"
                    rI.write(entry)
            with open(recapBatch, "w+") as f:
                batch = "\"C:/Program Files/Autodesk/Autodesk ReCap/Decap.exe\" --importWithLicense \"" + self.scanPath +"\" " + recapName + " --controlFile \"" + recapIndices + "\""
                f.write(batch)
                


    def exportCloud(self, exForm, logName, timestamp=True):
        if timestamp:
            if self.saveAllAtOnce == True:
                logFile = self.scanPath + "/" + logName
                export = " -C_EXPORT_FMT " + exForm + " -SAVE_CLOUDS ALL_AT_ONCE -LOG_FILE " + "\"" + logFile + "\""
                return export
            else:
                logFile = self.scanPath + "/" + logName
                export = " -C_EXPORT_FMT " + exForm + " -SAVE_CLOUDS -LOG_FILE " + "\"" + logFile + "\""
                return export
        else:
            if self.saveAllAtOnce == True:
                logFile = self.scanPath + "/" + logName
                export = " -C_EXPORT_FMT " + exForm + " -NO_TIMESTAMP -SAVE_CLOUDS ALL_AT_ONCE -LOG_FILE " + "\"" + logFile + "\""
                return export
            else:
                logFile = self.scanPath + "/" + logName
                export = " -C_EXPORT_FMT " + exForm + " -NO_TIMESTAMP -SAVE_CLOUDS -LOG_FILE " + "\"" + logFile + "\""
                return export

    def commandLineCreator(self):
        if self.operation1 == "DoNothing":
            self.operation1 = ""
        if self.operation2 == "DoNothing":
            self.operation2 = ""
        if self.saveAllAtOnce:
            i = 0
            for cloud in self.scansAll:
                cloud = self.scanPath + "/" + cloud
                logName = os.path.basename(cloud)
                logName = logName.split(".")
                logName = logName[0] + ".txt"
                if i == 0:
                    globalShift = "-GLOBAL_SHIFT AUTO "
                    self.ccCommand = self.prefix + self.openCloud(cloud, globalShift) + self.operation1 + self.operation2
                    i += 1
                else:
                    globalShift = "-GLOBAL_SHIFT FIRST "
                    self.ccCommand += self.openCloud(cloud, globalShift) + self.operation1 + self.operation2
                    i += 1
            self.ccCommand += self.exportCloud(self.exForm, logName)
        elif self.operationsSpecial == "Orthofoto":
            self.ccCommand = self.prefix
            i = 0

            for cloud in self.scansAll:
                cloud = self.scanPath + "/" + cloud
                logName = os.path.basename(cloud)
                logName = logName.split(".")
                logName = logName[0] + ".txt"
                globalShift = "-GLOBAL_SHIFT AUTO "
                self.ccCommand += self.openCloud(cloud, globalShift) + self.operation1
                i += 1
            self.ccCommand += self.clearClouds
        elif self.operationsSpecial == "-CROP2D-":
            self.ccCommand = self.prefix
            for cloud in self.scansAll:
                cloud = self.scanPath + "/" + cloud
                self.crop2DAutoCAD(cloud)
                self.ccCommand += self.exportCloud(self.exForm, logName = "Crop2D")
        else:
            globalShift = "-GLOBAL_SHIFT AUTO "
            i = 0


            for cloud in self.scansAll:
                cloud = str(cloud)
                cloud = self.scanPath + "/" + cloud
                logName = os.path.basename(cloud)
                logName = logName.split(".")
                logName = logName[0] + ".txt"
                if i == 0:
                    self.ccCommand = self.prefix + self.openCloud(cloud, globalShift) + self.operation1 + self.operation2 + self.exportCloud(self.exForm, logName) + self.clearClouds
                    i += 1
                else:
                    self.ccCommand += self.openCloud(cloud, globalShift) + self.operation1 + self.operation2 + self.exportCloud(self.exForm, logName) + self.clearClouds
                    i += 1
