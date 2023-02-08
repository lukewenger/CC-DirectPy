
import pyautocad
from pyautocad import APoint
import json
import re


class DrawJsn:
    def __init__(self,jsonPath):
        self.jsnLst = []
        self.autoCad = pyautocad.Autocad()
        with open(jsonPath) as j:
            j = j.read()
            j = re.split("({)",j)
        for jsn in j:
            entry = "{"
            entry+= jsn
            entry = entry.split("}")
            entry = entry[0]
            entry += "}"
            if len(entry) >=25:
                self.jsnLst.append(json.loads(entry))
            else:
                continue

    def drawCircle(self,diam=1):
        for jsn in self.jsnLst:
            if jsn["score"]>=0.9:
                __point = APoint(jsn["mittelPunkt"][0],jsn["mittelPunkt"][1])
                self.autoCad.model.AddCircle(__point,diam)
            else:
                print("unsure")








