import urllib

import requests
import http.cookiejar
import time
import os.path

try:
    from PIL import Image
except:
    pass

accept = 'application/json, text/javascript, */*; q=0.01'
agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

headers = {
    'Accept': accept,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.faxuan.net',
    'Origin': 'http://www.faxuan.net',
    'User-Agent': agent
}

HOME_PAGE_URL = 'http://www.faxuan.net/site/yunnan/'

session = requests.session()
cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)


def get_rid():
    return '2669d4dfbebbd2c8a80ce9f9112f6a01'
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    request = urllib.request.Request(HOME_PAGE_URL, None, headers)
    try:
        res = opener.open(request)
        page = res.read().decode()
        # print(page)
    except urllib.error.URLError as e:
        print(e.code, ':', e.reason)

    cookie.save(None, True, True)
    for item in cookie:
        # print(item.value)
        return item.value


def get_captcha():
    tt = str(int(time.time() * 1000))
    captcha_url = 'http://xf.faxuan.net/service/gc.html?tt=' + tt
    print(captcha_url)
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))

    captcha = input("pls input the captcha\n>")
    print("captcha: " + captcha)
    return captcha


def login(user_name, password):
    cookie.load(cookie_filename, True, True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    post_url = 'http://xf.faxuan.net/bss/service/userService!doUserLogin.do'
    post_data_values = {
        'userAccount': user_name,
        'userPassword': password,
        'code': get_captcha(),
        'rid': get_rid(),
        'key': 1
    }

    post_data = urllib.parse.urlencode(post_data_values).encode()
    print(post_data)
    get_request = urllib.request.Request(post_url, post_data, headers)
    get_response = opener.open(get_request)
    print(get_response.read().decode())


if __name__ == '__main__':
    user_name = '5306270870205'
    password = 'y888888'
    # get_rid()
    login(user_name, password)
