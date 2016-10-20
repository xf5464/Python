import codecs
import os
import time
import urllib
import urllib.error
import urllib.request
import socket

from lxml import etree

socket.setdefaulttimeout(5)

proxy_website = "http://www.xicidaili.com/nn/"

max_page = 5

ip_data = []

file_name = "ip_address.txt"

def run():

    while True:

        f = codecs.open(file_name, 'w', 'utf-8')
        f.close()

        ip_data.clear()

        for i in range(1, max_page):

            target_url = proxy_website

            if i > 1:

                target_url = proxy_website + str(i)


            _parse_page_data(target_url)

            time.sleep(5)

        for data in ip_data:
            if _is_alive(data):
                _write_to_record(data)

        time.sleep(600)


def _parse_page_data(url):
    page_data = _get_web_page_html(url)

    # t = pq(page_data)

    if (page_data == ""):
        time.sleep(2)
        _parse_page_data(url)
        return

    et = etree.HTML(page_data)

    result_odd = et.xpath('//tr[@class="odd"]')

    for i in result_odd:
        t2 = i.xpath("./td/text()")[:2]

        global ip_data

        ip_data.append([t2[0],t2[1]])
        print("IP:%s\tPort:%s" % (t2[0], t2[1]))

    print("end-")


def _get_web_page_html(url):
    html = _read_data(url)

    return html


def _read_data(url):
    try:
        html = urllib.request.urlopen(url).read().decode("utf-8")
        return html
    except urllib.error.URLError as e:
        return ""

def _write_to_record(data):
    f = codecs.open(file_name, 'a', 'utf-8')
    f.write(data[0] + " " + str(data[1]) + "\n")
    f.close()


#快代理
def _get_kuaidaili_ips():
    url = "http://www.kuaidaili.com/free/inha/"
    return

def _is_alive(data):
    ip = data[0]
    port = data[1]

    #proxy_support = urllib.request.ProxyHandler({'http': "127.0.0.1:80"})
    proxy_support = urllib.request.ProxyHandler({'http': ip + ":" + str(port)})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)

    try:
        #resp = opener.open("http://www.douban.com",None, 3)
        resp = urllib.request.urlopen("http://www.douban.com",None, timeout=3)

        if resp.code == 200:
            print("scccess " + ip)
            return True
        else:
            print("fail " + ip + " resp.code:" + str(resp.code))
            return False

    except:
         print("fail " + ip)
         return False


req_header2 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0','Referer':"www.xicidaili.com"}
opener = urllib.request.build_opener()
opener.addheaders = [req_header2]
urllib.request.install_opener(opener)

#run()
def _valid_ips():
    if not os.path.exists("ip_address2.txt"):
        return

    f = codecs.open("ip_address2.txt", 'r', 'utf-8')
    content = f.readlines()
    f.close()

    for line in content:
        k = str(line).split(" ")
        data = [k[0], int(k[1])]

        if _is_alive(data):
            _write_to_record(data)

_valid_ips()

print("done")