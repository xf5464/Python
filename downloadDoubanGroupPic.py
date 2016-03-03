#coding=utf-8
import urllib.request
import re
import os
import threading
import time


localPath = "e:/doubanDownLoad/group2/"

groupName = "haixiuzu"

maxPage = 1000

eachPageSize = 25

proxyList = ["39.83.13.122:8080", "113.68.87.45:8090", "171.39.234.222:80", "182.90.39.60:80"]

userProxyIndex = 0

proxies = {}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

def downloadGroupTopicPictures(groupName):

    changeProxy()

    global maxPage

    global eachPageSize

    print("start download group " + groupName + " topic pics total page " +  str(maxPage))

    parentFolder = localPath + groupName + "/"

    count = 0

    if not os.path.exists(parentFolder):
        os.makedirs(parentFolder)

    for i in range(0,maxPage):
        downloadOnePageTopPics(i*eachPageSize, parentFolder)

        count = count + 1

        if count >= 5:
            changeProxy()
            print("sleep 30s")
            time.sleep(30)
            count = 0

    print("download finished")

def downloadOnePageTopPics(startIndex, parentFolder):

    url = "https://www.douban.com/group/haixiuzu/discussion?start=" + str(startIndex)

    topicUrlSet = getTopicList(url)

    print("has elements:" + str(len(topicUrlSet)))

    for topicUrl in topicUrlSet:
        downloadOneTopicPictures(topicUrl, parentFolder)

    print("finish page " + str(startIndex + 1))

def getTopicList(url):

    decodeHtml = getWebPageHtml(url)
    
    topicPattern = re.compile(r"https://www.douban.com/group/topic/[0-9]+/")

    topsArray = topicPattern.findall(decodeHtml)

    topicSet = set(topsArray)

    return topicSet

def downloadOneTopicPictures(url, parentFolder):

    urls = getPicUrlInOneTopic(url)

    print("url:" + url + " len:" + str(len(urls)))

    for url in urls:
        downloadFile(url, parentFolder)

def getPicUrlInOneTopic(url):

    decodeHtml = getWebPageHtml(url)

    topicPattern = re.compile(r"https://img1.doubanio.com/view/group_topic/large/public/p[0-9]+.jpg")

    photoUrls = topicPattern.findall(decodeHtml)

    photoSet = set(photoUrls)

    return photoSet

def downloadFile(url, folder):
    #if not os.path.exists(localPath):
        #os.makedirs(localPath)

    startIndex = url.rfind("/")

    endIndex = url.rfind(".")

    imageName = url[startIndex:]

    data = urllib.request.urlopen(url).read()
   # data = urllib.FancyURLopener(proxies).open(url).read()

    f = open(folder + imageName,"wb")  
    f.write(data)  
    f.close()

def getWebPageHtml(url):

  #  proxy_handler = urllib.request.ProxyHandler({'http':"39.83.13.122:8080"})
   # opener = urllib.request.build_opener(proxy_handler)
    #urllib.request.install_opener(opener)
    page = urllib.request.urlopen(url)
    html = page.read()
    #req = urllib.request.Request(url=url, headers=headers)
   # html = req.urlopen(req).read()

    #global opener

    #proxy_handler = urllib.request.ProxyHandler({'http': proxyList[userProxyIndex]})
   # opener = urllib.request.build_opener(proxy_handler)
    #urllib.request.install_opener(opener)

    #html = opener.open(url).read()

    decodeHtml = html.decode("utf-8")

    return decodeHtml

def changeProxy():

    global proxies

    global userProxyIndex

   # proxies = {'http':proxyList[userProxyIndex]}

    print(getTimeStr() + " change proxy site;" + proxyList[userProxyIndex])
    #global opener

    #opener = urllib.FancyURLopener(proxies)

    proxy_handler = urllib.request.ProxyHandler({'http': proxyList[userProxyIndex]})
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)

    userProxyIndex = userProxyIndex + 1
    if userProxyIndex >= len(proxyList):
        userProxyIndex = 0

    print("userProxyIndex" + str(userProxyIndex))

def getTimeStr():
     return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

changeProxy()

downloadGroupTopicPictures(groupName)

