#coding=utf-8
import urllib.request
import re
import os
import threading
import time


localPath = "./group/"

groupName = "haixiuzu"

maxPage = 1

eachPageSize = 25

interval_time = 20 #20s刷一次首页

proxyList = ["39.83.13.122:8080", "113.68.87.45:8090", "171.39.234.222:80", "182.90.39.60:80"]

userProxyIndex = 0

proxies = {}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

def downloadGroupTopicPictures(groupName):

    #changeProxy()

    fetchCount = 0

    global maxPage

    global eachPageSize

    print("start download group " + groupName + " topic pics total page " +  str(maxPage))

    parentFolder = localPath + groupName + "/"

    count = 0

    if not os.path.exists(parentFolder):
        os.makedirs(parentFolder)

    while True:
        #定时去取第一页
        print(_get_time_string() + " fetchCount:" + str(fetchCount))

        for i in range(0,maxPage):
            #找到第一个已经存在的时候，break
            downloadOnePageTopPics(groupName, i*eachPageSize, parentFolder)

        fetchCount = fetchCount + 1

        time.sleep(interval_time)

    print("download finished")

def downloadOnePageTopPics(groupName, startIndex, parentFolder):

    url = "https://www.douban.com/group/" + groupName + "/discussion?start=" + str(startIndex)

    print(_get_time_string() + " check url")

    topicUrlSet = getTopicList(url)

    print("has elements:" + str(len(topicUrlSet)))

    for topicUrl in topicUrlSet:

        _topic_info = _get_topic_info(topicUrl)

        date = _topic_info[0]

        author = _topic_info[1]

        title = _topic_info[2] \

        if author == "":
            continue

        _sub_folder_name =  title + "-by-" + author

        _full_folder_name = parentFolder + "/" + date + "/" + _translate_file_Name(_sub_folder_name)

        if os.path.exists(_full_folder_name):
            continue
        else:
            os.makedirs(_full_folder_name)

        print(_get_time_string() + ":" + " load" + title + " by" + author)

        downloadOneTopicPictures(topicUrl, _full_folder_name)

    print("finish page " + str(startIndex + 1))

    return True

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

def _get_topic_info(url):

    decodeHtml = getWebPageHtml(url)

    dateInfoPattern = re.compile(r"\<span class=\"color-green\">.*\<\/span\>")

    dateInfoData = dateInfoPattern.findall(decodeHtml)

    if len(dateInfoData) == 0:
        return ("", "", "")

    index1 = dateInfoData[0].find(">")

    index2 = dateInfoData[0].find(" ", index1)

    date = dateInfoData[0][index1 + 1:index2]

    titlePattern = re.compile(r"h1>.*</h1>", re.S)

    tileInfo = titlePattern.findall(decodeHtml)

    title = ""

    author = ""

    if len(tileInfo) >= 1:
         titlePattern2 = re.compile(r"\n.*\n")

         z = titlePattern2.findall(tileInfo[0])

         z1 = z[0].replace("\n", "")

         z1 = z1.strip()

         title = z1

    authorPattern1 = re.compile(r"<span class=\"from\">.*</a>")

    authorInfo = authorPattern1.findall(decodeHtml)

    authorName = ""

    if len(authorInfo) >= 1:
        index1 = authorInfo[0].find(">")

        index2 = authorInfo[0].find(">", index1 + 1)

        index3 = authorInfo[0].find("<", index2)

        authorName = authorInfo[0][index2 + 1:index3]

    ret = (date, authorName,title)

    return ret

def getPicUrlInOneTopic(url):

    decodeHtml = getWebPageHtml(url)

    topicPattern = re.compile(r"https://img[0-9]*.doubanio.com/view/group_topic/large/public/p[0-9]+.jpg")

    photoUrls = topicPattern.findall(decodeHtml)

    photoSet = set(photoUrls)

    return photoSet

def downloadFile(url, folder):
    #if not os.path.exists(localPath):
        #os.makedirs(localPath)

    startIndex = url.rfind("/")

    endIndex = url.rfind(".")

    imageName = _translate_file_Name(url[startIndex:])

    try:
        data = urllib.request.urlopen(url).read()
    except urllib.error.URLError as e:
        return

   # data = urllib.FancyURLopener(proxies).open(url).read()

    f = open(folder  + "/" + imageName,"wb")
    f.write(data)  
    f.close()

def getWebPageHtml(url):

  #  proxy_handler = urllib.request.ProxyHandler({'http':"39.83.13.122:8080"})
   # opener = urllib.request.build_opener(proxy_handler)
    #urllib.request.install_opener(opener)

    try:
        html = urllib.request.urlopen(url).read()
    except urllib.error.URLError as e:
        return ""

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

def _translate_file_Name(_file_name):
    r1 = re.compile("\\\|\*|\<|\>|\||\?|\/")
    return re.sub(r1, "a",  _file_name)

def _get_time_string():
    return time.strftime('%Y-%m-%d %H:%M:%S')
#changeProxy()

downloadGroupTopicPictures(groupName)

