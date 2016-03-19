# coding=utf-8
import os
import codecs
import chardet

targetEncode = "utf-8"

needRecursive = 1  # 子文件里面的也要处理的话设置成1，只处理当前目录设置成0

def processtxtfile(targetfile):
    print("start " + targetfile)

    newfile = open(targetfile, "rb")  # 要有"rb"，如果没有这个的话，默认使用gbk读文件。
    # buf = file.read()

    buf = newfile.readlines()

    maxline = min(len(buf), 20)

    temp = ""

    for i in range(0, maxline):
        temp += buf[i]

    newfile.close()
    result = chardet.detect(temp)

    print("file:" + targetfile + " result:" + str(result["encoding"]) + " " + str(result["confidence"]))
    readencode = result["encoding"]

    if readencode == "GB2312":  # 加大容错率
        readencode = "gbk"
    encodefile = codecs.open(targetfile, "r", readencode)

    encodestring = ""

    try:
        encodestring = encodefile.read()
    except UnicodeDecodeError, e:
        gbkfile = codecs.open(targetfile, "r", "gbk")
        try:
            encodestring = gbkfile.read()
            gbkfile.close()
        except UnicodeDecodeError, e2:
            print("error:" + str(e2))
            # continue

    utf8string = encodestring

    if not isinstance(utf8string, unicode):
        utf8string = unicode(encodestring, targetEncode)

    encodefile.close()

    tt = utf8string.encode(targetEncode)

    # continue
    newwritefile = open(targetfile, "w")
    newwritefile.write(tt)
    newwritefile.close()

    print("end " + targetfile)
    # file = open(file,"r",encoding=result["encoding"])


def processfolder(folder):

    _real_path = folder

    if not isinstance(folder, unicode):
        _real_path = unicode(folder,'gbk')

    files = os.listdir(_real_path)

    for subfile in files:
        if subfile.find(".txt") != -1:
            processtxtfile(_real_path + "\\" + subfile)
        elif subfile.find(".") == -1 and needRecursive == 1:
            processfolder(_real_path + "\\" + subfile)
    return


processfolder(os.getcwd())
