from django.test import TestCase
import json, os
# Create your tests here.
def readJson(filename):
    fileJson = open(filename, "r")
    reportData = json.loads(fileJson.read())
    fileJson.close()
    os.remove(fileJson.name)
    return reportData

a=readJson("P:\Document\ProjectTotNghiep\code\Do_An_Tot_Nghiep_NLP\PlagismDetector\DEF\\result\\4cuong.docx4.json")
print(a)