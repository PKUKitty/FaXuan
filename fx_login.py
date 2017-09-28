# coding=utf-8
import urllib
import urllib2

import requests
import cookielib
import time
import os.path

from pytesseract import pytesseract
from selenium import webdriver

try:
    from PIL import Image, ImageEnhance
except:
    pass

accept = 'application/json, text/javascript, */*; q=0.01'
agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/61.0.3163.79 Chrome/61.0.3163.79 Safari/537.36'
# agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36';

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.faxuan.net',
    'Origin': 'http://www.faxuan.net',
    'User-Agent': agent
}

HOME_PAGE_URL = 'http://www.faxuan.net/site/yunnan/'

session = requests.session()

cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)


def get_rid():
    return '3510b8894ac3147f7df1b26f7b34c213'
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    request = urllib2.Request(HOME_PAGE_URL, None, headers)
    try:
        res = opener.open(request)
        page = res.read().decode()
        # print(page)
    except urllib2.URLError as e:
        print(e.errno, ':', e.reason)

    cookie.save(None, True, True)
    for item in cookie:
        # print(item.value)
        return item.value


def get_captcha(timestamp):
    captcha_url = 'http://xf.faxuan.net/service/gc.html?timestamp=' + timestamp
    print(captcha_url)
    r = opener.open(captcha_url).read()
    # r = requests.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r)
        f.close()
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'pls change directory %s captcha.jpg ' % os.path.abspath('captcha.jpg'))

    captcha = raw_input("pls input the captcha\n>")
    print("captcha: " + captcha)
    return captcha


def login(user_name, password):
    post_url = 'http://www.faxuan.net/shop/api/xf_login'
    tt = str(int(time.time() * 1000))
    post_data_values = {
        'user_name': user_name,
        'user_pass': password,
        'code': get_captcha(tt),
        'rid': get_rid(),
        # 'key': 13
    }

    data = urllib.urlencode(post_data_values)

    # get_url = 'http://xf.faxuan.net/bss/service/userService!doUserLogin.do?userAccount=' + user_name + '&userPassword=' + password + '&code=' + data + '&rid=' + get_rid() + '&key=1'
    # print get_url

    request = urllib2.Request(post_url, data, headers)

    try:
        response = opener.open(request)
        result = response.read().decode('gb2312')
        print result
    except urllib2.HTTPError, e:
        print e.code

        # resp = requests.post(post_url, headers=headers, cookies=requests.utils.dict_from_cookiejar(data[1]),
        #                      data=post_data_values)
        # # resp = requests.get(get_url, headers=headers, cookies=requests.utils.dict_from_cookiejar(cookies))
        # print(resp.content)


def get_cookies():
    res = requests.get('http://www.faxuan.net/site/yunnan/')
    # print res.content
    return res.cookies


def ger_random_qq():
    return '12345678'  # TODO


if __name__ == '__main__':
    user_name = '15094279360'
    password = 'y888888'
    # get_cookies()

    # login(user_name, password)

    driver = webdriver.Firefox()
    driver.get(HOME_PAGE_URL)
    time.sleep(1)
    cookie1 = driver.get_cookies()

    elem_user = driver.find_element_by_id('user_name')
    elem_psw = driver.find_element_by_id('user_pass')
    elem_code = driver.find_element_by_id('code')

    # image_name = '/Users/yujun/PycharmProjects/FaXuan/login.png'
    image_name = 'home_page.png'
    driver.get_screenshot_as_file(image_name)
    img = Image.open(image_name)
    box = (285, 380, 345, 415)
    region = img.crop(box)
    region.save('captcha.png')
    im = Image.open('captcha.png')
    imgry = im.convert('L')
    sharpness = ImageEnhance.Contrast(imgry)
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save('captcha.png')

    # captcha = raw_input("pls input the captcha\n>")
    captcha = pytesseract.image_to_string(sharp_img)
    print 'captcha:'
    print captcha

    is_login = False
    if captcha:
        elem_user.send_keys(user_name)
        elem_psw.send_keys(password)
        elem_code.send_keys(captcha)
        click_login = driver.find_element_by_class_name('login_button')
        click_login.click()
        cookie2 = driver.get_cookies()
        if cookie1 != cookie2:
            is_login = True

    else:
        driver.quit()
        exit()
    # if not is_login:
    #     print 'login failed'
    #     driver.quit()  # TODO
    #     exit()

    # click to modify profile,
    time.sleep(2)
    current_window = driver.current_window_handle
    modifyProfile = driver.find_element_by_xpath("//a[contains(@href, ‘navindex’)]")
    modifyProfile.get_attribute("href")
    modifyProfile.click()
    user_info_qq = driver.find_element_by_id('userinfoQQ')
    user_info_qq.send_keys(ger_random_qq())

    user_info_save = driver.find_element_by_id('userInfo_2_queren')
    user_info_save.click()
    # time sleep
    time.sleep(1)

    user_info_confirm = driver.find_element_by_id('popalertConfirm')
    user_info_confirm.click()
    time.sleep(3)

    time.sleep(10)
    driver.quit()
    exit()

    my_study = driver.find_element_by_link_text('javascript:base.index2(1)')
    my_study.click()
    time.sleep(3)

    # click must course
    must_courses = driver.find_element_by_id('bxCourse')
    must_courses.click()

    # start study
    # include all must courses
    country_security = driver.find_element_by_link_text('中华人民共和国国家安全法》...')
    country_security.click()
    time.sleep(3)

    start = time.time()
    duration = 30 * 60
    # country_security_timer = driver.find_element_by_id('timer')
    while True:
        if time.time() - start > duration:
            break
        else:
            time.sleep(10)
            continue
    exit_study = driver.find_element_by_link_text('退出学习')
    exit_study.click()

    exit_study_confirm = driver.find_element_by_id('popwinConfirm')
    exit_study_confirm.click()
    time.sleep(1)

    # must courses
    constitution = driver.find_element_by_link_text('宪法知识读本')
    constitution.click()
    time.sleep(3)

    start = time.time()
    while True:
        if time.time() - start > duration:
            break
        else:
            time.sleep(10)
            continue
    constitution_exit_study = driver.find_element_by_link_text('退出学习')
    constitution_exit_study.click()

    constitution_exit_study_confirm = driver.find_element_by_id('popwinConfirm')
    constitution_exit_study_confirm.click()
    time.sleep(1)

    # must courses
    yunnan = driver.find_element_by_link_text('云南省农村扶贫开发条例')
    yunnan.click()
    time.sleep(3)

    start = time.time()
    while True:
        if time.time() - start > duration:
            break
        else:
            time.sleep(10)
            continue
    yunnan_exit_study = driver.find_element_by_link_text('退出学习')
    yunnan_exit_study.click()

    yunnan_exit_study_confirm = driver.find_element_by_id('popwinConfirm')
    yunnan_exit_study_confirm.click()
    time.sleep(1)

    # start
    country_security = driver.find_element_by_link_text('中华人民共和国国家安全法》...')
    country_security.click()
    time.sleep(3)

    course_exs = driver.find_element_by_link_text('课程练习')
    course_exs.click()

    start_exs = driver.find_element_by_link_text('开始练习')
    start_exs.click()

    time.sleep(20)
    submit_exs = driver.find_element_by_link_text('提交练习')
    submit_exs.click()

    driver.quit()
