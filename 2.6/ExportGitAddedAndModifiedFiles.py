#coding=utf-8
import subprocess
import os
import shutil

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

gitRepositoryPath = "E:/j6/fresh/resource/"

outputPath = "f:/git输出/"

startCommitSign = "931d78f7ed1372aa5c598b20f35180f19089b04c"

endCommitSign = "0cd9b397c63c6999932418008bfe68d19b6df8d5"

def copyFilesToDestination(log):
    files = str(log).split("\n")

    count = 0

    for fileUrl in files:
        desFolderUrl = ""

        indexOfSlash = fileUrl.rfind("/")

        if indexOfSlash != -1:
            desFolderUrl = outputPath + fileUrl[0:fileUrl.rfind("/")]
        else:
            desFolderUrl = outputPath

        realStartPath = unicode(gitRepositoryPath + fileUrl, "utf8")

        realDesPath = unicode(desFolderUrl, "utf8")

        if not os.path.exists(realDesPath):
            os.makedirs(realDesPath)

        print(unicode(str(gitRepositoryPath + fileUrl), "utf8"))

        if not fileUrl.__contains__("."): #folder not file:
            continue

        if fileUrl == "":
            print("file url is empty")
        else:
            if os.path.exists(realStartPath):#判断下文件是否存在，不存在会报错
                # shutil.copyfile(realStartPath, realFileDesPath)
                shutil.copy(realStartPath, realDesPath)

        count = count + 1

    print("total files:" + str(count))

#[(A|C|D|M|R|T|U|X|B)
def gitStatus(startCommit, endCommit, repoDir):
    cmd = 'git diff --name-only --diff-filter=ACMR %s %s %s'%(endCommit,startCommit,repoDir)
    pipe = subprocess.Popen(cmd, shell=True, cwd=repoDir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
    (out, error) = pipe.communicate()
    #print out,error
    copyFilesToDestination(out)
    pipe.wait()
    return

gitStatus(startCommitSign,endCommitSign, gitRepositoryPath)