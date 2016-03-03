#coding=utf-8

import sys
import os
import glob
import time

def main(argv):

    print(argv)

    t = 1

    if len(argv) > 1:
        ChinesePath = argv[1]
        VietnamPath = argv[2]
        forceUpdateTxtPath = ""
        if len(argv) > 3:
            forceUpdateTxtPath = argv[3]


def comparePath(chinesePath, vietnamPath, forceUpdateTxtFilePath):

    chinesePropertyDic = getPropertyFiles(chinesePath)

    vietnamDic = getPropertyFiles(vietnamPath)

    nameKeys = chinesePropertyDic.keys()

    newFiles = []

    currentPath = os.curdir + "/" + getTimeStr()

    if not os.path.exists(currentPath):
        os.makedirs(currentPath)

    print("output path:" + currentPath)

    for key in nameKeys:
        if not vietnamDic.__contains__(key):
            chineseFileData = open(chinesePropertyDic[key]).read()

            print("add file:" + key)

            writeNewFile(currentPath + "/" + key, chineseFileData)
        else:
            chineseDic = readOnePropertyFileToDic(chinesePropertyDic[key])

            vientamDic = readOnePropertyFileToDic(vietnamDic[key])

            hasNewAttribute = False

            chinesePropertyKeys = chineseDic["propertyKeys"]
            vientamKeys = vientamDic["propertyKeys"]

            chinesePropertyValues = chineseDic["propertyValues"]
            vientamValues = vientamDic["propertyValues"]

            newObjects = []

            for i in range(0,len(chinesePropertyKeys)):
                if not vientamKeys.__contains__(chinesePropertyKeys[i]):
                    newObjects.append({"key":chinesePropertyKeys[i], "value":chinesePropertyValues[i]})

            if len(newObjects) > 0:

                writeData = ""

                for i in range(0,len(vientamKeys)):
                    writeData =  writeData + str(vientamKeys[i]) + "=" + str(vientamValues[i]) + "\n"

                newLength = len(newObjects)

                for j in range(0, newLength):
                    newObj = newObjects[j]

                    if j < newLength - 1:
                         writeData = writeData + str(newObj["key"]) + "=" + str(newObj["value"]) + "\n"
                    else:
                         writeData = writeData + str(newObj["key"]) + "=" + str(newObj["value"])

            writeNewFile(currentPath + "/" + key, writeData)


def getPropertyFiles(filePath):

    newpath = filePath + "/*.properties"

    files = glob.glob(newpath)

    ret = {}

    for f in files:
        ret[os.path.basename(f)] = f

    return ret

def readOnePropertyFileToDic(file):
    fileData=  open(file, "r").readlines()
    print(file)
    print(fileData)

    ret = {}

    keys = []

    values = []

    for obj in fileData:
        index1 = obj.find("=")
        index2 = obj.find("\n")

        if index1 == -1:
            continue

        key =  obj[0:index1]

        if index2 == -1:
            index2 = len(obj)

        value = obj[index1 + 1:index2]

        keys.append(key)

        values.append(value)
        print("key:" + key + " value:" + value)

    ret["propertyKeys"] = keys

    ret["propertyValues"] = values

    return ret

def writeNewFile(filePath, fileData):

     print("write file path:" + filePath)

     print("write file data:" + fileData)

     newFile = open(filePath, "w")

     newFile.write(fileData)

     newFile.close()

def getTimeStr():
     return time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))

if __name__ == '__main__':
   main(sys.argv)



comparePath("F:/testLan/chinese", "F:/testLan/vientam", "")




