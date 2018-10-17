#-*- coding: utf-8 -*-

'''
#참고사항
- 지금까지의 모든 거래 기록을 2017-01-01 부터 현재 날짜까지 다운로드 (변경가능)
- 다운로드 경로는 브라우저가 기본으로 설정된 다운로드 위치 (Download 폴더)
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import xlrd
from collections import OrderedDict

#0 Login
chrome_options = webdriver.ChromeOptions()

prefs = {
        "profile.default_content_setting_values.plugins": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        "PluginsAllowedForUrls": "http://www.ssobing.com"
}

chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument("--disable-features=EnableEphemeralFlashPermission")

#For OSX
#chrome_path = '/usr/local/bin/chromedriver'
chrome_path = 'C:/Users/ALEXa/AppData/Local/Programs/Python/chromedriver.exe'

driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

def ssobing_login(id, pw):
    driver.get('http://www.ssobing.com/selleradmin/login/index')

    input_id = driver.find_element_by_xpath("//input[contains(@name, 'main_id')]")
    input_pw = driver.find_element_by_xpath("//input[contains(@name, 'main_pwd')]")

    input_id.send_keys(id)
    input_pw.send_keys(pw)

    login = driver.find_element_by_xpath("//input[contains(@class, 'submit_btn')]")
    login.send_keys(Keys.ENTER)

    driver.get('http://www.ssobing.com/selleradmin/goods/regist')

#2 정보 세팅
def download_setting():

    driver.get("http://www.ssobing.com/selleradmin/order/catalog")
    driver.maximize_window()

    selectall_btn = driver.find_elements_by_xpath("//span[@class='icon-check hand all-check']")

    start = '2018-09-01'
    end = '2018-10-01' #오늘 날짜로 fix

    #시작일을 2017-01-01로 설정, 마감일은 수집하는 날짜로 서버가 자동설정 해줌
    #input에 .send_keys가 아니라 value 값을 바꾸는 javascript를 실행해야 함
    collecting_date = driver.find_elements_by_xpath("//input[@name='regist_date[]']")
    driver.execute_script("arguments[0].setAttribute('value','2017-01-01')", collecting_date[0]) #변경가능

    selectall_btn[0].click() #Before 출고
    selectall_btn[1].click() #After 출고 이후

    start_collect_btn = driver.find_elements_by_xpath("//button[@type='submit']")
    start_collect_btn[0].click()

def download_action():
    time.sleep(3)

    #전체선택
    select_ops = driver.find_elements_by_xpath("//span[@class='custom-select-box-btn btn drop_multi_main']")
    select_ops[0].click()
    time.sleep(2)

    #양식선택
    select_form = driver.find_element_by_xpath("//select[@id='select_down_35']")
    time.sleep(2)
    select_btn = driver.find_element_by_xpath("//span[@class='custom-select-box-btn btn drop']")
    select_btn.click()
    time.sleep(3)
    select_basic = driver.find_elements_by_xpath("//span[contains(text(), '기본양식_파인애플')]")
    select_basic[0].click()

    #Download
    down_btn = driver.find_element_by_xpath("//button[@name='excel_down']")
    down_btn.click()

    #Delivery
    deliv_methods = driver.find_elements_by_xpath("//input[@name='excel_search_shipping_method[]']")
    for i in deliv_methods:
        i.click()

    #final_download
    final_down = driver.find_element_by_xpath("//span[@class='btn large gray']")
    final_down.click()
