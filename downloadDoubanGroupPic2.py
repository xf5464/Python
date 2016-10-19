#coding=utf-8
import codecs
import os
import random
import re
import time
import urllib.request
import socket

localPath = "./group2/"

groupName = "haixiuzu"

maxPage = 1000

eachPageSize = 25

interval_time = 30 #20s刷一次首页

opener = 1

proxyList = ["39.83.13.122:8080", "113.68.87.45:8090", "171.39.234.222:80", "182.90.39.60:80"]

userProxyIndex = 0

proxies = {}
req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
 'Accept-Encoding':'gzip',
 'Connection':'keep-alive',
 'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
 }

req_header2 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0','Referer':None}
"""
opener = urllib.request.build_opener()
opener.addheaders = [req_header2]
urllib.request.install_opener(opener)
"""

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

fileList = {}

txt_name = "downLoadedTopics.txt"

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

    for i in range(100, maxPage):

        validNum = downloadOnePageTopPics(groupName, i * eachPageSize, parentFolder)

        sleep_time = random.randint(interval_time*0.5, interval_time)

        print("finish page " + str(i + 1))

        print("sleep" + str(sleep_time) + "s")

        time.sleep(sleep_time)



    print("download finished")

def downloadOnePageTopPics(groupName, startIndex, parentFolder):

    url = "https://www.douban.com/group/" + groupName + "/discussion?start=" + str(startIndex)

    #url = "http://localhost/aaa.html"

    validNum = 0

    print(_get_time_string() + " check url")

    ret = getTopicList(url)

    if len(ret) == 0:
        return

    topsArray = ret[0]
    titles = ret[1]
    authors = ret[2]

    #topicUrlSet = getTopicList(url)

    length = len(topsArray)

    print("has elements:" + str(length))

    for i in range(0, length):

        topicUrl = topsArray[i]

        if i >= len(authors) or i >= len(titles):
            print("ERROR downloadOnePageTopPics out of index i:" + str(i) + " titles.len:" + str(len(titles)) + " authors.len:" + str(len(authors)))
            return validNum

        author = authors[i]

        title = titles[i]

        if author == "":
            continue

        _sub_folder_name =  title + "-by-" + author

        if  fileList.get(_sub_folder_name) == True:
            continue

        _topic_info = _get_topic_info(topicUrl)

        date = _topic_info[0]

        if date == "":
            continue

        _full_folder_name = parentFolder + "/" + date + "/" + _translate_file_Name(_sub_folder_name)

        if os.path.exists(_full_folder_name):
            continue
        else:
            try:
                 os.makedirs(_full_folder_name)
            except NotADirectoryError as e:
                print("---NotADirectoryError--:" + _full_folder_name)
                continue

        print(_get_time_string() + ":" + " load" + title + " by" + author)

        downloadOneTopicPictures(topicUrl, _full_folder_name, _sub_folder_name)

        validNum = validNum + 1

        time.sleep(random.randint(1, 4))

    return validNum

def getTopicList(url):

    #把帖子名称和用户名也取出来，这样就可以减少很多次数去取具体页面
    decodeHtml = getWebPageHtml(url)

    tablePattern = re.compile(r"<table class=\"olt\">.*</table>", re.S)

    tableStringArray = tablePattern.findall(decodeHtml)

    if len(tableStringArray) == 0:
        return []

    targetString = tableStringArray[0]

    topicPattern = re.compile(r"https://www.douban.com/group/topic/[0-9]+/")

    topsArray = topicPattern.findall(decodeHtml)

    """
    topicSet = []

    for id in topsArray:
        if id not in topicSet:
            topicSet.append(id)
    """

    titlePattern = re.compile(r'(?<= title=\").*?(?=\")')

    titles = titlePattern.findall(targetString)

    #sciprit有一个
    del titles[0]

    authorPattern = re.compile(r'(?<=class=\"\">).*(?=</a></td>)')

    authors = authorPattern.findall(targetString)

    #topicSet = list(set(topsArray))

    #topicSet.sort(topsArray.index)

    ret = [topsArray, titles, authors]
    return ret

def downloadOneTopicPictures(url, parentFolder, _sub_folder_name):

    urls = getPicUrlInOneTopic(url)

    print("url:" + url + " len:" + str(len(urls)))

    for url in urls:

        downloadFile(url, parentFolder)

        time.sleep(1)

    _write_to_record(_sub_folder_name)

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
        data = _read_data(url)
    except urllib.error.URLError as e:
        print("urllib.error.URLError:" + url)
        return

   # data = urllib.FancyURLopener(proxies).open(url).read()
    try:
        f = open(folder  + "/" + imageName,"wb")
        f.write(data)
        f.close()
    except FileNotFoundError as e:
        return

def getWebPageHtml(url):

  #  proxy_handler = urllib.request.ProxyHandler({'http':"39.83.13.122:8080"})
   # opener = urllib.request.build_opener(proxy_handler)
    #urllib.request.install_opener(opener)

    try:
        html = _read_data(url)
    except urllib.error.URLError as e:
        return ""

    #ecodeHtml = html.decode("utf-8")

    return html

def getTimeStr():
     return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def _translate_file_Name(_file_name):
    r1 = re.compile("\\\|\*|\<|\>|\||\?|\/")
    return re.sub(r1, "a",  _file_name)

def _get_time_string():
    return time.strftime('%Y-%m-%d %H:%M:%S')
#changeProxy()

def _readFileList():
    if not os.path.exists(txt_name):
        return

    f = codecs.open(txt_name, 'r', 'utf-8')
    content = f.readlines()
    f.close()

    for line in content:
        fileList[line.encode('utf-8')] = True

def _write_to_record(name):
    fileList[name] = True

    f = codecs.open(txt_name, 'a', 'utf-8')
   #txt = unicode("campeón\n", "utf-8")
    f.write(name + "\n")
    f.close()

def _changeProxy():

    # return
    print("aaaa")

    global opener
    #proxy_support = urllib.request.ProxyHandler({'http':'119.254.84.90:80'})
    proxy_support = urllib.request.ProxyHandler({'http': '127.0.0.1:80'})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)

    return

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

def _read_data(url):
    try:

        response = opener.open(url);
        response_data = response.read().decode("utf8")
       # print(proxyIp, "正确：" + response_data);
        #html = urllib.request.urlopen(url).read()
        return response_data
    except urllib.error.URLError as e:
        return ""

hostname = socket.gethostname()

ipList = socket.gethostbyname_ex(hostname)

_changeProxy()

ipList2 = socket.gethostbyname_ex(hostname)
#_readFileList()
#t = _read_data("www.baidu.com")
print("bvbbb")
#t2 =  _read_data("http://www.douban.com")
t3 = 1
#_write_to_record("九个")
downloadGroupTopicPictures(groupName)

