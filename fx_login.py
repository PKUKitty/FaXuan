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


def modify_profile(profile_driver):
    modifyProfile = profile_driver.find_element_by_xpath(".//div[@class='userimg']/a")
    modifyProfile.get_attribute("href")
    modifyProfile.click()

    user_info_address = profile_driver.find_element_by_id('userAddress')
    user_info_address.send_keys('beijing')
    print 'user address qq end'

    time.sleep(2)
    current_win = profile_driver.current_window_handle
    user_info_save = profile_driver.find_element_by_id('userInfo_2_queren')
    user_info_save.click()
    print 'user info 2 queren'

    time.sleep(2)
    current_win = profile_driver.current_window_handle
    user_info_confirm = profile_driver.find_element_by_id('popalertConfirm')
    user_info_confirm.click()
    print 'alert confirm'


def study_course(course_driver, course_name):
    my_study = course_driver.find_element_by_xpath(".//a[contains(@href, 'base.index2(1)')]")
    my_study.get_attribute('href')
    my_study.click()
    time.sleep(5)
    print 'click my study'
    # driver.switch_to.window(driver.window_handles[-1])

    # click must course
    # must_courses = driver.find_element_by_id('bxCourse')
    # must_courses.click()

    # start study
    # include all must courses
    course_name = course_driver.find_element_by_xpath('/html/body/div/div/ul/li/div/a')
    course_name.get_attribute('href')
    course_name.click()
    time.sleep(3)

    # exs
    driver.switch_to.window(driver.window_handles[-1])
    exs_click = course_driver.find_element_by_xpath(".//ul[@class='coursetab clear']/li[3]")
    exs_click.click()
    print 'exs_click end'

    start_exs_click = course_driver.find_element_by_xpath(".//a[contains(@href, '1103')]")
    start_exs_click.get_attribute('href')
    start_exs_click.click()
    time.sleep(1)

    course_driver.switch_to.window(driver.window_handles[-1])
    time.sleep(10)

    commit_exs_click = course_driver.find_element_by_xpath(".//a[contains(@href, 'myCommit')]")
    commit_exs_click.get_attribute('href')
    commit_exs_click.click()
    time.sleep(1)

    current_win = driver.current_window_handle
    exit_exs_confirm = course_driver.find_element_by_id('popwinConfirm')
    exit_exs_confirm.get_attribute('href')
    exit_exs_confirm.click()
    print 'exit_exs_confirm'

    # close tab
    course_driver.close()

    start = time.time()
    duration = 30 * 60
    while True:
        if time.time() - start > duration:
            break
        else:
            time.sleep(10)
            continue

    course_driver.switch_to.window(driver.window_handles[-1])
    exit_study = course_driver.find_element_by_xpath(".//a[contains(@href, 'exitStudy')]")
    exit_study.get_attribute('href')
    exit_study.click()
    print 'exit study'

    time.sleep(1)
    current_win = driver.current_window_handle
    exit_study_confirm = driver.find_element_by_id('popwinConfirm')
    # exit_study_confirm.get_attribute('href')
    exit_study_confirm.click()
    print 'exit_study_confirm'


def captchaProcessor():
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

    captcha = pytesseract.image_to_string(sharp_img)
    return captcha.replace(' ', '')  # replace all space
    print 'captcha:'
    print captcha


if __name__ == '__main__':
    user_name = '15094279360'
    password = 'y888888'
    # get_cookies()

    # login(user_name, password)

    driver = webdriver.Firefox()
    driver.get(HOME_PAGE_URL)
    time.sleep(1)

    elem_user = driver.find_element_by_id('user_name')
    elem_psw = driver.find_element_by_id('user_pass')
    elem_code = driver.find_element_by_id('code')

    is_login = False
    login_times = 0

    while login_times < 10:
        captcha = captchaProcessor()
        if len(captcha) == 4:
            elem_user.send_keys(user_name)
            elem_psw.send_keys(password)
            elem_code.send_keys(captcha)
            click_login = driver.find_element_by_class_name('login_button')
            click_login.click()
            time.sleep(5)

            if len(driver.window_handles) == 2:
                is_login = True
                break
            else:
                current_win = driver.current_window_handle
                close_button = driver.find_element_by_class_name('close_button')
                close_button.get_attribute('href')
                time.sleep(1)
                close_button.click()
                time.sleep(1)

                # refresh captcha
                change_testword = driver.find_element_by_class_name('change_testword')
                change_testword.get_attribute('href')
                change_testword.click()
                time.sleep(1)
                login_times = login_times + 1
                print 'login times: ' + str(login_times)

                elem_user.clear()
                elem_psw.clear()
                elem_code.clear()
        else:
            # refresh captcha
            change_testword = driver.find_element_by_class_name('change_testword')
            change_testword.get_attribute('href')
            change_testword.click()
            time.sleep(1)
            login_times = login_times + 1
            print "login times: " + str(login_times)

            elem_user.clear()
            elem_psw.clear()
            elem_code.clear()

    if not is_login:
        print 'login failed'
        driver.quit()  # TODO
        exit()

    # click to modify profile,
    time.sleep(10)
    driver.switch_to.window(driver.window_handles[-1])

    # modify_profile(driver)

    study_course(driver, "aaaa")

    study_course(driver, "aaaa")

    time.sleep(10)
    driver.quit()
    exit()
