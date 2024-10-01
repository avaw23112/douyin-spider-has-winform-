'''
Author: avaw23112 1214113371@qq.com
Date: 2024-09-29 17:15:38
LastEditors: avaw23112 1214113371@qq.com
LastEditTime: 2024-10-01 20:05:04
FilePath: \CODE_py\PYTHON\spider\爬虫脚本\自己的尝试\抖音搜索进入.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import re
import requests
from urllib.parse import unquote
import json
import os
from pprint import pprint
import sys
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.exceptions import Timeout
#到时候接入api更改就行

session = requests.Session()
retry = Retry(connect=5, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)   

kw = "斯卡蒂s".encode("utf-8")
url_kw = f"https://www.douyin.com/search/{kw}"

#考虑到安全性，不应该有默认值才对
header_single = {
    "cookie":"",
    "user-agent":"",
    "referer":url_kw
}

down_directory = "."

#内置一个下载计数器，和admid随时比较，到数即停
user_admid = 0      
images_admid = 25   
user_count = 0      #以下载的作者数为计数
images_count = 0     #以下载的图片个数为计数

def Get_single(original_count=15,original_offset=0):
    global user_admid
#网页端开始的视频数量为15，增量为0
    set_count = original_count
    set_offset = original_offset
    single_url =f"https://www.douyin.com/aweme/v1/web/general/search/single/"
    single_data = {
        "device_platform": "webapp",
        "aid": 6383,
        "channel": "channel_pc_web",
        "search_channel": "aweme_general",
        "enable_history": 1,
        "keyword": kw,
        "search_source": "normal_search",
        "query_correct_type": 1,
        "is_filter_search": 0,
        "offset": set_offset,
        "count": set_count,
    }
    try:
        res = session.get(url=single_url,headers=header_single,data=single_data)
    except Timeout:
        print(f"请求 {single_url} 超时")
    except requests.exceptions.ConnectionError:
        print(f"无法连接到 {single_url}")
    except requests.exceptions.RequestException as e:
        # 其他请求相关的异常
        print(f"请求出错: {e}")
    #这里可以优化，用正则表达式只把aweme_infor这一栏找出来，避免加载没必要的数据
    json_str = unquote(res.text)
    json_data = json.loads(json_str)
    aweme_infor_list = json_data['data']
    #因为优化程度不高，于是不并行处理了
    for aweme_infor in aweme_infor_list:
        if 'aweme_info' not in aweme_infor:
            continue
        temp = aweme_infor['aweme_info']
        aweme_id = temp['aweme_id']
        desc = temp['desc']
        sec_uid = temp['author']['sec_uid']
        nick_name =  temp['author']['nickname']
        if user_admid == 0 :
            user_admid = 999
        json_data_user = Get_MS4(aweme_id=aweme_id,sec_uid=sec_uid)
        flag = Download_image(json_data=json_data_user,desc=desc,kw=kw,nick_name=nick_name)
        if flag == False:
            return
    res.close() 

user_header = {
    "cookie":"",
    "user-agent":"",
    "referer":"https://www.douyin.com/"
}

def Get_MS4(aweme_id,sec_uid):
    MS4_url = f"https://www.douyin.com/user/{sec_uid}?modal_id={aweme_id}"
    RE = re.compile(r'<script id="RENDER_DATA" type="application/json">(?P<wurl>.*?)</script>')
    res = session.get(url=MS4_url,headers=user_header)
    grp = RE.search(res.text)
    list = grp.groupdict()
    str1 = list["wurl"]
    json_str = unquote(str1)
    json_data = json.loads(json_str)
    res.close()
    return json_data

def Download_image(json_data,nick_name,desc,kw):
    global user_count
    global images_count

    image_list = json_data['app']['videoDetail']['images']
    i = 0
    if image_list == []:
        return True

    #先检测有没有作者目录
    down_path = os.path.join('down_directory', nick_name)
    if not os.path.exists(down_path):
        os.makedirs(down_path)
        user_count += 1
    elif user_count >= user_admid: 
        print("已经达到要求的user下载数")
        return False
    # 再检测有没有关键词目录
    kw_path = bytes(kw).decode("utf-8")  # 确保编码和解码一致
    full_path = os.path.join(down_path, kw_path)  # 使用 os.path.join 来连接路径
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    
    for image_index in image_list:
        if images_count >= images_admid:
            print("已经达到要求的image下载数")
            return False
        url = image_index['urlList'][2]
        filename = desc + str(i) + '.jpeg'
        file_path = os.path.join(full_path,filename)
        with open(file_path,mode="wb") as f:
            res = session.get(url=url,headers=user_header)
            cont = res.content
            f.write(cont)
            res.close()
        i +=1
        images_count += 1 
    return True


def ALLIN():
    #初次启动 
    Get_single()
    #网页刷新规律是offset 15,count 0
    #之后offset为10，count为25,35,...每次+10增量
    for count in range(25,images_admid,10):
        #抽象的一逼，一次刷15张不行，刷135就行
        Get_single(count,135)


def init(keyword,cookie,user_agentc,dic,u_a,i_a):
    global kw
    global url_kw
    global header_single
    global user_header
    global down_directory
    global user_admid    
    global images_admid 
    kw = str(keyword).encode("utf-8")
    down_directory = dic
    user_admid = int(u_a)
    images_admid = int(i_a)

    url_kw = f"https://www.douyin.com/search/{kw}"
    header_single["cookie"] = cookie
    header_single["user-agent"]=user_agentc
    header_single["referer"]=url_kw
    user_header["cookie"]= cookie
    user_header["user-agent"]=user_agentc

    return


if __name__ == '__main__':
    init(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
    ALLIN()

