import mitmproxy.http
import sys
from mitmproxy import ctx
import numpy as np
import cv2

sys.path.append("C:/Users/Administrator/AppData/Local/Programs/Python/Python37/lib/site-packages/")

ctx.log.info(sys.executable)
ctx.log.info('.'.join(sys.path))


class Counter:
    def __init__(self):
        self.num = 0
        self.load_urls = set()

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        #ctx.log.info("We've seen %d flows" % self.num)

    def response(self, flow: mitmproxy.http.HTTPFlow):

        url = flow.request.url

        if url.find("_c.png") != -1 or url.find("_d.png") != -1:

            t1 = url.rfind("/")

            file_name = url[t1 + 1:len(url)]

            self.load_urls.add(file_name)

            ctx.log.info(">>>>>response:" + file_name)

            local_folder = "f:/zhaocha/"

            local_path = local_folder + file_name

            image = open(local_path,"wb")
            image.write(flow.response.content)

            if url.find("_c.png") != -1:
                another_file_name = file_name.replace("_c","_d")
                complex_file_name = file_name.replace("_c","_e")
                complex_file_name2 = file_name.replace("_c","_f")
            else:
                another_file_name = file_name.replace("_d","_c")
                complex_file_name = file_name.replace("_d","_e")
                complex_file_name2 = file_name.replace("_d","_f")

            if another_file_name in self.load_urls:
                another_image = cv2.imread(local_folder + another_file_name)
                now_image = cv2.imread(local_path)

                outputGrey1 = cv2.cvtColor(another_image, cv2.COLOR_BGR2GRAY)

                outputGrey2 = cv2.cvtColor(now_image, cv2.COLOR_BGR2GRAY)

                outputGrey = outputGrey2 - outputGrey1

                eq2 = cv2.equalizeHist(outputGrey)  # 灰度图像直方图均衡化
                im_color = cv2.applyColorMap(outputGrey, cv2.COLORMAP_JET)

                cv2.imwrite(local_folder + complex_file_name, im_color)

                ret_image = open(local_folder + complex_file_name, "rb").read()
                flow.response.content = ret_image



addons = [
    Counter()
]