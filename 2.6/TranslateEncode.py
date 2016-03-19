#coding=utf-8
import os
import codecs
import chardet
import math

from chardet.universaldetector import UniversalDetector

targetEncode = "utf-8"

files = os.listdir(os.getcwd())

def getDecode(file, maxLine):
     newFile = open(file, "rb")#要有"rb"，如果没有这个的话，默认使用gbk读文件。
     # buf = file.read()

     buf = newFile.readlines()

     if maxLine == -1:
         maxLine = len(buf)

     max = min(len(buf), maxLine)

     temp = ""

     for i in range(0,max):
         temp = temp + buf[i]

     newFile.close()
     result = chardet.detect(temp)
     return result


print("total:" + str(len(files)))
for file in files:
    #print(file)
    if file.find(".txt") != -1:


        print("start " + file)

        newFile = open(file, "rb")#要有"rb"，如果没有这个的话，默认使用gbk读文件。
       # buf = file.read()

        buf = newFile.readlines()

        max = min(len(buf), 20)

        temp = ""

        for i in range(0,max):
           temp = temp + buf[i]

        newFile.close()
        result = chardet.detect(temp)

        print("file:" + file + " result:" +str(result["encoding"]) + " " + str(result["confidence"]))
        readEncode = result["encoding"]

        if readEncode == "GB2312":
            readEncode = "gbk"
        encodeFile = codecs.open(file, "r", readEncode)

        try:
            encodeString = encodeFile.read()
        except UnicodeDecodeError, e:
           # newDecode = getDecode(file, -1)
            errorString = str(e)
            errorStringPeriod = errorString[e.start:e.end]

            gbkFile = codecs.open(file, "r", "gbk")
            try:
                encodeString = gbkFile.read()
                gbkFile.close()
            except UnicodeDecodeError, e2:
                print("error:" + str(e2))
            #continue

        utf8String = encodeString;

        if not isinstance(utf8String, unicode):

            utf8String = unicode(encodeString, "utf-8")

        encodeFile.close();

        tt = utf8String.encode("utf-8")

        #continue
        kk = chardet.detect(tt)
        newWriteFile = open(file, "w")
        newWriteFile.write(tt)
        newWriteFile.close();

        print("end " + file)
        #file = open(file,"r",encoding=result["encoding"])