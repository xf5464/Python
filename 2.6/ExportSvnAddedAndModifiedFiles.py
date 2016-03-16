#coding=utf-8
import pysvn
import shutil
import os

#http://pysvn.tigris.org/project_downloads.html 去这里根据svn版本和python版本下载对应的pySvn库

client = pysvn.Client()

#svn根目录
svnPath = "E:/测试/"
#svnPath = "E:/suitang/fresh/resource/"

#输出目录
outputPath = "f:/svnExport5/"

#起始svn版本号
startRevisionId = 129827

#结束svn版本号
endRevisionId = 129829

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

        realFileDesPath = unicode(outputPath + fileUrl, "utf8")

        if not os.path.exists(realDesPath):
            os.makedirs(realDesPath)

        if os.path.exists(realStartPath):#判断下文件是否存在，不存在会报错
            # shutil.copyfile(realStartPath, realFileDesPath)
            shutil.copy(realStartPath, realDesPath)

        count = count + 1

        print(str(svnType) + " " + unicode(str(svnPath + fileUrl), "utf8"))

print("complete " + str(count))