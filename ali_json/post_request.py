import urllib.request
import urllib.parse
import json
import time
import base64
import os
import codecs


def read_img(img_item):
    with open(img_item, 'rb') as f:  # 以二进制读取本地图片
        data = f.read()
        encodestr = str(base64.b64encode(data),'utf-8')
    #请求头
    # 请修改为你自己的appcode，可从云市场订单或者api网关处获得
    AppCode = ""
    headers = {
        'Authorization': 'APPCODE ' + AppCode,
        'Content-Type': 'application/json; charset=UTF-8'
    }

    return encodestr, headers

def posturl(url,headers,data={}):
    try:
        params=json.dumps(data).encode(encoding='UTF8')
        req = urllib.request.Request(url, params, headers)
        r = urllib.request.urlopen(req)
        html =r.read()
        r.close();
        return html.decode("utf8")
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
    time.sleep(1)

def post(img_item, json_path):
    url_request="https://ocrapi-subject.taobao.com/ocrservice/subject"

    encodestr, headers = read_img(img_item)

    dict = {'img': encodestr}

    html = posturl(url_request,headers, data=dict)
    #print(html)

    tmp_path = img_item.split('/')[-1].split('.')
    file_path = tmp_path[0] + '.' + tmp_path[1 ]+ ".json"
    with codecs.open(json_path + file_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    img_path = './train/imgs/'
    json_path = './train/json/'

    for item in os.listdir(img_path):
        post(img_path+item, json_path)
