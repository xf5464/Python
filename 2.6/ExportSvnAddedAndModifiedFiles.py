#coding=utf-8
import pysvn
import shutil
import os

#http://pysvn.tigris.org/project_downloads.html 去这里根据svn版本和python版本下载对应的pySvn库

client = pysvn.Client()

#svn根目录
#svnPath = "E:/tool/测试/"
svnPath = "E:/suitang/fresh/resource/"

#输出目录
outputPath = "f:/svnExport3/"

#起始svn版本号
startRevisionId = 129787

#结束svn版本号
endRevisionId = 129812

svnAddedType = "added"

svnModifiedType = "modified"

summary = client.diff_summarize( svnPath,
                                 pysvn.Revision(pysvn.opt_revision_kind.number, startRevisionId),
                                 svnPath,
                                 pysvn.Revision(pysvn.opt_revision_kind.number,endRevisionId))

count = 0

for object in summary:
    svnType = str(object.summarize_kind)
    fileUrl = str(object.path)

    if svnType == svnAddedType or svnType == svnModifiedType:
        desFolderUrl = ""

        indexOfSlash = fileUrl.rfind("/")

        if indexOfSlash != -1:
            desFolderUrl = outputPath + fileUrl[0:fileUrl.rfind("/")]
        else:
            desFolderUrl = outputPath

        realStartPath = unicode(svnPath + fileUrl, "utf8")

        realDesPath = unicode(desFolderUrl, "utf8")

        if not os.path.exists(realDesPath):
            os.makedirs(realDesPath)

        shutil.copy(realStartPath, realDesPath)

        count = count + 1

        print("svntype::" + str(svnType) + " fileUrl:" + str(svnPath + fileUrl))

print("complete " + str(count))