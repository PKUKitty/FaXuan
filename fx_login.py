# coding=utf-8
import json
import logging
import logging.handlers
import time
import os.path
import random

# import redis
import urllib

import datetime
from pytesseract import pytesseract
from selenium import webdriver
from PIL import Image, ImageEnhance

from selenium.webdriver import DesiredCapabilities

import send_email
from config import Config
from redis_processor import RedisProcessor

HOME_PAGE_URL = 'http://www.faxuan.net/site/yunnan/'


def get_option_num(option_str):
    if option_str == "A":
        return "1"
    if option_str == "B":
        return "2"
    if option_str == "C":
        return "3"
    if option_str == "D":
        return "4"


def query_redis(question, q_type):
    redis = RedisProcessor()
    if q_type == '单选题':
        res = redis.get_single_choice(question)
        if res is None:
            return str(random.randint(1, 4))
    if q_type == '多选题':
        res = redis.get_multi_choice(question)
        if res is None:
            return ['1', '2', '3', '4']
    if q_type == '判断题':
        res = redis.get_true_false(question)
        if res is None:
            return False


def parse_config(file_name):
    config_file = open(file_name)
    json_config = json.load(config_file)
    config_file.close()
    return json_config


def ger_random_qq():
    qq = ''
    for i in range(0, 9):
        qq = qq + str(random.randint(1, 9))
    return qq


def modify_profile(profile_driver):
    modify_pro = profile_driver.find_element_by_xpath(".//div[@class='userimg']/a")
    modify_pro.get_attribute("href")
    modify_pro.click()

    time.sleep(5)
    user_info_address = profile_driver.find_element_by_id('userAddress')
    user_info_address.clear()
    input_address = "China Beijing"
    user_info_address.send_keys(input_address)

    user_info_qq = profile_driver.find_element_by_id('userinfoQQ')
    user_info_qq.clear()
    user_info_qq.send_keys(ger_random_qq())

    time.sleep(5)
    var = profile_driver.current_window_handle
    user_info_save = profile_driver.find_element_by_id('userInfo_2_queren')
    user_info_save.click()

    time.sleep(10)
    current_win = profile_driver.current_window_handle
    user_info_confirm = profile_driver.find_element_by_id('popalertConfirm')
    user_info_confirm.click()


def study_course(course_driver, course_name):
    driver.switch_to.window(driver.window_handles[-1])
    my_study = course_driver.find_element_by_xpath(".//a[contains(@href, 'base.index2(1)')]")
    my_study.get_attribute('href')
    my_study.click()
    time.sleep(5)
    logger.debug("click my study")
    # driver.switch_to.window(driver.window_handles[-1])

    # click must course
    # must_courses = driver.find_element_by_id('bxCourse')
    # must_courses.click()

    # start study
    # include all must courses
    course_name = course_driver.find_element_by_xpath('/html/body/div/div/ul/li/div/a/h3')
    course_name.get_attribute('href')
    course_name.click()
    time.sleep(5)

    # exs
    driver.switch_to.window(driver.window_handles[-1])
    exs_click = course_driver.find_element_by_xpath(".//ul[@class='coursetab clear']/li[3]")
    exs_click.click()
    logger.debug("exs_click end")
    time.sleep(5)

    start_exs_click = course_driver.find_element_by_xpath(".//a[contains(@href, '2165')]")
    start_exs_click.get_attribute('href')
    start_exs_click.click()
    time.sleep(5)

    # TODO input the exs answer
    # 去掉、(单选题)前缀
    each_question = course_driver.find_element_by_id('ti_title').text
    each_question_type = each_question[2:4]
    each_question_str = each_question[6:]

    res = query_redis(each_question_str, each_question_type)
    if each_question_type == '单选题':
        for idx in range(0, 3):
            xpath = ".//ul[@id='ti_item']/li[" + str(idx + 1) + "]"
            # 去掉A、
            option = course_driver.find_element_by_xpath(xpath)
            if option.text[2:] == res:
                option.click()
                break
    if each_question_type == '多选题':
        for idx in range(0, 3):
            xpath = ".//ul[@id='ti_item']/li[" + str(idx + 1) + "]"
            # 去掉A、
            option = course_driver.find_element_by_xpath(xpath)
            if option.text[2:] in res:  # array
                option.click()
    if each_question_type == '判断题':
        if res == 1:  # 对
            xpath_tmp = ".//ul[@id='ti_item']/li[1]"
        else:
            xpath_tmp = ".//ul[@id='ti_item']/li[2]"
        course_driver.find_element_by_xpath(xpath_tmp).click()

    # TODO input the exs answer

    course_driver.switch_to.window(driver.window_handles[-1])
    time.sleep(10)

    commit_exs_click = course_driver.find_element_by_xpath(".//a[contains(@href, 'myCommit')]")
    commit_exs_click.get_attribute('href')
    commit_exs_click.click()
    time.sleep(5)

    current_win = driver.current_window_handle
    exit_exs_confirm = course_driver.find_element_by_id('popwinConfirm')
    exit_exs_confirm.get_attribute('href')
    exit_exs_confirm.click()
    logger.debug("exit_exs_confirm")

    # write exs into redis
    paper_key_value = {}
    current_page = 0
    tmp_count = 0
    redis_processor = RedisProcessor()
    while current_page < 5 and tmp_count < 10:
        xpath = ".//ul[@id='result']/li[" + str(tmp_count + 1) + "]/h3"
        question = course_driver.find_element_by_xpath(xpath)
        question_str = question.text[7:]
        if tmp_count == 9:
            question_str = question.text[8:]

        logger.debug('question: ' + question_str)

        # <strong>正确答案：A　　用户选择：</strong>
        ans_xpath = ".//ul[@id='result']/li[" + str(tmp_count + 1) + "]/div/strong"
        answer_str = course_driver.find_element_by_xpath(ans_xpath).text[5:6]
        # A->1,B->2,C->3,D->4
        answer_num = get_option_num(answer_str)
        option_xpath = ".//ul[@id='result']/li[" + str(tmp_count + 1) + "]/ul/li[" + answer_num + "]"
        option_str = course_driver.find_element_by_xpath(option_xpath).text[2:]
        logger.debug('answer: ' + option_str)
        if question_str and option_str:
            redis_processor.insert_single_choice(question_str, option_str)
        tmp_count = tmp_count + 1

    # close tab
    course_driver.close()

    start = time.time()
    duration = 20 * 60
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
    logger.debug("exit study")

    time.sleep(5)
    # current_win = driver.current_window_handle
    exit_study_confirm = driver.find_element_by_id('popwinConfirm')
    # exit_study_confirm.get_attribute('href')
    exit_study_confirm.click()
    logger.debug("exit_study_confirm")


def captcha_processor():
    hp_image_name = 'home_page.png'
    driver.get_screenshot_as_file(hp_image_name)
    img = Image.open(hp_image_name)
    box = (285, 380, 345, 415)
    region = img.crop(box)

    captcha_img_name = 'captcha.png'
    region.save(captcha_img_name)
    # get img source
    # captcha_img = driver.find_element_by_id('captcha')
    # captcha_img_src = captcha_img.get_attribute('src')
    # urllib.urlretrieve(captcha_img_src, captcha_img_name)

    im = Image.open(captcha_img_name)
    imgry = im.convert('L')
    sharpness = ImageEnhance.Contrast(imgry)
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save(captcha_img_name)

    captcha_code = pytesseract.image_to_string(sharp_img)

    if os.path.exists(hp_image_name):
        os.remove(hp_image_name)
    if os.path.exists(captcha_img_name):
        os.remove(captcha_img_name)

    return captcha_code.replace(' ', '')  # replace all space


if __name__ == '__main__':

    config = Config.get_instance()
    user_name = config.get_str('user0', 'user_name')
    password = config.get_str('user0', 'password')

    LOG_FILE = '/home/yujun/PycharmProjects/FaXuan/fx_login.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger('fx_login')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # redis_conn = redis.Redis(host='127.0.0.1', port=6379, db=0)

    each_day_task_complete = False
    RESET_TASK_STATUS_TIME = "00"
    TASK_STUDY_COURSE_TIME = "22"
    TASK_RE_LOGIN_TIME = '%02d' % ((int(TASK_STUDY_COURSE_TIME) + 2) % 24)

    while True:
        now_hour = datetime.datetime.now().strftime('%H')

        if now_hour == RESET_TASK_STATUS_TIME:
            # reset status
            each_day_task_complete = False

        if not each_day_task_complete and (now_hour == TASK_STUDY_COURSE_TIME or now_hour == TASK_RE_LOGIN_TIME):
            firefox_capabilities = DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True
            firefox_capabilities['binary'] = '/usr/local/bin/geckodriver'

            driver = webdriver.Firefox(capabilities=firefox_capabilities,
                                       log_path='/home/yujun/PycharmProjects/FaXuan/geckodriver.log')
            driver.get(HOME_PAGE_URL)
            time.sleep(5)

            elem_user = driver.find_element_by_id('user_name')
            elem_psw = driver.find_element_by_id('user_pass')
            elem_code = driver.find_element_by_id('code')

            is_login = False
            login_times = 0

            while login_times < 20:
                captcha = captcha_processor()
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
                        logger.debug('login times: ' + str(login_times))

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
                    logger.debug("login times: " + str(login_times))

                    elem_user.clear()
                    elem_psw.clear()
                    elem_code.clear()

            if not is_login:
                logger.debug("login failed")
                driver.quit()
                # exit()

            # driver.maximize_window()
            # click to modify profile,
            time.sleep(20)

            if now_hour == TASK_STUDY_COURSE_TIME:
                driver.switch_to.window(driver.window_handles[-1])

                # modify_profile(driver)

                logger.debug("-----course 1-------")
                study_course(course_driver=driver, course_name="aaaa")

                logger.debug("-----course 2-------")
                study_course(driver, "aaaa")

            if now_hour == TASK_RE_LOGIN_TIME:
                driver.switch_to.window(driver.window_handles[-1])
                my_home_page = driver.find_element_by_xpath(".//a[contains(@href, 'base.index2(0)')]")
                my_home_page.get_attribute('href')
                my_home_page.click()
                time.sleep(1)

                today_point = driver.find_element_by_id('todypoint')
                today_point_text = today_point.text

                today_total_point = driver.find_element_by_id('todaytpoint')
                today_total_point_text = today_total_point.text

                point_rank = driver.find_element_by_id('pointRank')
                point_rank_text = point_rank.text

                test_send_email = send_email.SendEmail()
                test_send_email.send_msg(today_point_text + ";" + today_total_point_text + ";" + point_rank_text)

                each_day_task_complete = True

            time.sleep(10)
            driver.quit()

        else:
            time.sleep(60)
            continue
