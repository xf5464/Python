import codecs
import os
import re
import socket
import time
import urllib
import urllib.error
import urllib.request

from lxml import etree

socket.setdefaulttimeout(3)

proxy_website = "http://www.xicidaili.com/nn/"

max_page = 5

ip_address_text_name = "ip_address.txt"

ip_address_text_backup_name = "ip_address_backup.txt"

ip_dict = set()

def run():

    while True:

        _valid_old_proxy()

        _get_ip_from_xicilidaili()

        _get_kuaidaili_ips()

        _backup_ips()

        print("finish one time")

        time.sleep(600)

def _backup_ips():
    f = codecs.open(ip_address_text_name, 'r', 'utf-8')
    content = f.readlines()
    f.close()

    back_file = codecs.open(ip_address_text_backup_name, 'w', 'utf-8')
    back_file.writelines(content);
    back_file.close()

def _valid_old_proxy():
    ret = _read_old_ips()

    _clear_ip_address_text()

    count = 0

    for data in ret:
        if _is_alive(data):
            _write_to_record(data)
            count = count + 1

    print("old data complete success count=" + str(count))

def _get_ip_from_xicilidaili():

    count = 0

    print("start get from xicilidaili")
    for i in range(1, max_page):
        target_url = proxy_website

        target_url = proxy_website + str(i)

        ip_data = _parse_page_data(target_url)

        for data in ip_data:
            if _is_alive(data):
                _write_to_record(data)
                count = count + 1

        time.sleep(2)

    print("end get from xicilidaili")

    print("finish read xicidaili success count:" + str(count))

def _clear_ip_address_text():
    f = codecs.open(ip_address_text_name, 'w', 'utf-8')
    f.close()

    ip_dict.clear()

def _parse_page_data(url):

    proxy_support = urllib.request.ProxyHandler(None)
    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = req_header2
    urllib.request.install_opener(opener)

    page_data = _get_web_page_html(url)

    # t = pq(page_data)

    if (page_data == ""):
        time.sleep(2)
        _parse_page_data(url)
        return

    et = etree.HTML(page_data)

    result_odd = et.xpath('//tr[@class="odd"]')

    ip_data = []

    for i in result_odd:
        t2 = i.xpath("./td/text()")[:2]

        ip_data.append([t2[0],t2[1]])
        print("read IP:%s\tPort:%s" % (t2[0], t2[1]))

    return ip_data


def _get_web_page_html(url):
    ret = _read_data(url)

    if isinstance(ret, str):
        return ret

    try:
         html = _read_data(url).decode("utf-8")
    except:
         html = ""

    return html


def _read_data(url):
    try:

        html = urllib.request.urlopen(url).read()
        return html
    except urllib.error.URLError as e:
        return ""

def _write_to_record(data):

    if data[0] in ip_dict:
        return

    f = codecs.open(ip_address_text_name, 'a', 'utf-8')
    f.write(data[0] + " " + str(data[1]) + "\n")
    f.close()

    ip_dict.add(data[0])


#快代理
def _get_kuaidaili_ips():

    print("start _get_kuaidaili_ips")
    base_url = "http://www.kuaidaili.com/free/inha/"

    success_count = 0

    for i in range(1, 6):
        target_url = base_url + str(i)

        proxy_support = urllib.request.ProxyHandler(None)
        opener = urllib.request.build_opener(proxy_support)
        # opener.addheaders = req_header3
        urllib.request.install_opener(opener)


        page_data = _get_web_page_html(target_url)

        try:
            et = etree.HTML(page_data)
        except:
            print("error _get_kuaidaili_ips:" + target_url)

            if page_data != "":
                re_pattern = re.compile(r'(?<=data-title=\"IP\">).*?(?=</td>)')
                temp_ips = re.findall(page_data)
                print(len(temp_ips))
            continue

        result_ips = et.xpath('//td[@data-title="IP"]')
        result_ports = et.xpath('//td[@data-title="PORT"]')

        for j in range(0, len(result_ips)):
            ip_element = result_ips[j];
            k = ip_element.xpath("./text()")

            if len(k) == 0:
                continue

            if j >= len(result_ports):
                continue

            port_element = result_ports[j]
            k2 = port_element.xpath("./text()")

            if (len(k2)) == 0:
                continue

            ip_data = [k[0],k2[0]]

            if _is_alive(ip_data):
                _write_to_record(ip_data)
                success_count = success_count + 1

    print("end _get_kuaidaili_ips success_count:" + str(success_count))
    return


def _is_alive(data):
    ip = data[0]
    port = data[1]

    #proxy_support = urllib.request.ProxyHandler({'http': "127.0.0.1:80"})
    proxy_support = urllib.request.ProxyHandler({'http': ip + ":" + str(port)})
    opener = urllib.request.build_opener(proxy_support)
    # opener.addheaders = req_header3
    urllib.request.install_opener(opener)

    try:
        #resp = opener.open("http://www.douban.com",None, 3)
        start_time = time.time()
        resp = urllib.request.urlopen("http://www.douban.com",None, timeout=3)

        if resp.code == 200:
            print("scccess " + ip)
            return True
        else:
            print("fail " + ip + " resp.code:" + str(resp.code))
            return False

    except:
         # print("fail " + ip)
         end_time = time.time()

         print("timeout cost:" + str(end_time - start_time))
         return False



req_header2 =  [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'),('Referer',"http://www.xicidaili.com/nn/1")]
req_header3 =  [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'),('Referer',"http://www.kuaidaili.com/free/inha/1/")]

#run()
def _read_old_ips():
    if not os.path.exists(ip_address_text_name):
        return

    ret = []

    f = codecs.open(ip_address_text_name, 'r', 'utf-8')
    content = f.readlines()
    f.close()

    for line in content:
        k = str(line).split(" ")
        ip = k[0];
        port = k[1]
        ret.append([ip,int(port)])

    return ret

#_valid_ips()

#_get_kuaidaili_ips()#
run()
#_backup_ips()