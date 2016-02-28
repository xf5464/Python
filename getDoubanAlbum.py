#coding=utf-8
import urllib.request
import re
import os


localPath = "e:/doubanDownLoad/"

count = 0

username = "SlimWei"

def downloadUserPhotos(userName):
        
    print("开始下载" + userName + "的相册")
    userPageUrl = "https://www.douban.com/people/" + userName + "/photos"


    #得到相册列表
    albumList = getUserAlbumList(userPageUrl, userName)

    retKeys = albumList.keys()

    for tempKey in retKeys:
        downLoadOneAlbumPhotos(tempKey, userName, albumList[tempKey])
        
    print("下载完成")

def getUserAlbumList(url, userName):

    firstPageAlumnList = getOnePageAlumnList(url)

    page = urllib.request.urlopen(url)
    html = page.read()

    decodeHtml = html.decode("utf-8")
    
    leftPagePattern = re.compile(r"https://www.douban.com/people/" + userName + "/photos\?start\=[0-9]+")

    leftPhotoPages = leftPagePattern.findall(decodeHtml);

    leftPhotoPageSet = set(leftPhotoPages);

    for leftPageUrl in leftPhotoPageSet:
        leftPageAlumnList = getOnePageAlumnList(leftPageUrl)

        keys = leftPageAlumnList.keys()

        for key in keys:
            firstPageAlumnList[key] = leftPageAlumnList[key]
        
    return firstPageAlumnList

def getOnePageAlumnList(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    
    pattern = re.compile(r"https://www.douban.com/photos/album/[0-9]+/\"\>(?!\<img).*\<")

    decodeHtml = html.decode("utf-8")
    
    ret = pattern.findall(decodeHtml);

    temp = set(ret)

    ret = {}
    
    for oneUrl in temp:
        index1 = oneUrl.find("album/")

        index2 = oneUrl.find("/", index1 + 7)

        albumId = oneUrl[index1 + 6:index2]

        index3 = oneUrl.rfind(">");

        index4 = oneUrl.rfind("<");

        albumName = oneUrl[index3 + 1:index4]

        ret[albumId] = albumName
                 
    return ret


def getCurrentAlbumHtml(url):
    #得到相册当前页面html
    page = urllib.request.urlopen(url)
    html = page.read()
    
    return html

def downLoadOneAlbumPhotos(albumId, username, albumName):
    #根据相册id下载当前相册的所有图片
    print("开始下载相册 " + albumName + " albumId:" + albumId)
    startUrl = "https://www.douban.com/photos/album/" + str(albumId);

    global count
    
    count = 0
    
    parentFolder = localPath + username + "/" + str(albumName).rstrip()

    if not os.path.exists(parentFolder):
        os.makedirs(parentFolder)
        
    html = getCurrentAlbumHtml(startUrl)

    leftPhotoPageUrls = getPageUrlsOfOneAlnum(startUrl, html);

    downLoadOnePagePhotoOfOneAlbum(startUrl, parentFolder)

    for url in leftPhotoPageUrls:
        downLoadOnePagePhotoOfOneAlbum(url, parentFolder)

def downLoadOnePagePhotoOfOneAlbum(url, parentFolder):
    #下载相册一页的图片
    
    page = urllib.request.urlopen(url)
    html = page.read()

    photoUrls = getCurrentPhotoPageUrls(html)

    for photoUrl in photoUrls:
        bigPhotoUrl = getOnePhotoUrl(photoUrl)

        downloadFile(bigPhotoUrl, parentFolder)

        global count
        
        count = count + 1
        
    
    
def getPageUrlsOfOneAlnum(firstPageUrl, sourceHtml):
    #https://www.douban.com/photos/album/68058307/?start=18

    subUrl = firstPageUrl + "/\?start=[0-9]+"
    
    #得到类似这样的地址
    pattern = re.compile(subUrl)

    decodeHtml = sourceHtml.decode("utf-8")
    
    urls = pattern.findall(decodeHtml)

    setUrl = set(urls)

    return setUrl

def getCurrentPhotoPageUrls(sourceHtml):
    pattern = re.compile(r"https://www.douban.com/photos/photo/[0-9]+")

    decodeHtml = sourceHtml.decode("utf-8")
    
    ret = pattern.findall(decodeHtml);

    return ret

def getOnePhotoUrl(url):
    #得到一张图片的url
    # page url https://www.douban.com/photos/photo/2322109721
    # image url https://img3.doubanio.com/view/photo/photo/public/p2320432016.jpg
    startIndex = url.rfind("/")

    photoNum = url[startIndex + 1:]

    ret = "https://img3.doubanio.com/view/photo/photo/public/p" + photoNum + ".jpg"
    
    return ret

def getImageUrl(html):
    pattern = re.compile(r"https://img3.doubanio.com/view/photo/.*jpg")

    decodeHtml = html.decode("utf-8")
    
    ret = pattern.findall(decodeHtml);

    return ret

def downloadFile(url, folder):
    #if not os.path.exists(localPath):
        #os.makedirs(localPath)

    startIndex = url.rfind("/")

    endIndex = url.rfind(".");

    imageName = url[startIndex:]

    data = urllib.request.urlopen(url).read()  
    f = open(folder + imageName,"wb")  
    f.write(data)  
    f.close()
    

downloadUserPhotos(username)

#downLoadOneAlbumPhotos(alumnId)

#for eachPhotoUrl in currentPagePhotoUrls:
 #  downloadFile(getOnePhotoUrl(eachPhotoUrl))

#imageUrls = getImageUrl(html);

#for oneImageUrl in imageUrls:
  #  downloadFile(oneImageUrl)

#print(html)
