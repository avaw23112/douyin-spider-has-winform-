'''
Author: avaw23112 1214113371@qq.com
Date: 2024-09-28 18:39:16
LastEditors: avaw23112 1214113371@qq.com
LastEditTime: 2024-10-01 18:19:45
FilePath: \CODE_py\PYTHON\spider\爬虫脚本\自己的尝试\抖音爬取图片.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import re
import requests
from urllib.parse import unquote
import json
import os
from pprint import pprint
import sys


class a :
    def Get_html(self):
        res = requests.get(self.url,headers=self.header)
        RE = re.compile(r'<script id="RENDER_DATA" type="application/json">(?P<wurl>.*?)</script>')
        grp = RE.search(res.text)
        list = grp.groupdict()
        str1 = list["wurl"]
        json_str = unquote(str1)
        json_data = json.loads(json_str)
        res.close()
        return json_data

    #根据作者名，新开一个目录
    def Download_image(self,json_data):
        artist = json_data['app']['videoDetail']['authorInfo']['nickname']
        down_path = os.path.join(self.down_directory, artist)
        if not os.path.exists(artist):
            os.makedirs(artist)

        #把图片全部放入目录内
        image_list = json_data['app']['videoDetail']['images']
        i = 0
        for image_index in image_list:
            url = image_index['urlList'][2]
            filename = 'image' + str(i) + '.jpeg'
            file_path = os.path.join(down_path, filename)
            with open(file_path,mode="wb") as f:
                f.write(requests.get(url=url,headers=self.header).content)
            i +=1
        
    def __init__(self,urlc,cookie,user_agentc,dic):
        self.down_directory =dic
        self.url = urlc
        self.header = {"referer":"https://www.douyin.com/"}
        self.header["cookie"] = cookie
        self.header["user-agent"]=user_agentc
        return


if __name__ == '__main__':
    urlc = sys.argv[1]
    cookie = sys.argv[2]
    user_agent = sys.argv[3]
    dic = sys.argv[4]
    a = a(urlc,cookie,user_agent,dic)
    json_data = a.Get_html()  
    a.Download_image(json_data=json_data)
    print("下载完成")


