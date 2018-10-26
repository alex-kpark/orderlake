from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import xlrd

# Set Driver
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

# 다운로드 함수 선언
def ssobing_download(id, pw):

    driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

    driver.get('http://www.ssobing.com/selleradmin/login/index')

    input_id = driver.find_element_by_xpath("//input[contains(@name, 'main_id')]")
    input_pw = driver.find_element_by_xpath("//input[contains(@name, 'main_pwd')]")

    input_id.send_keys(id)
    input_pw.send_keys(pw)

    login = driver.find_element_by_xpath("//input[contains(@class, 'submit_btn')]")
    login.send_keys(Keys.ENTER)

    driver.get('http://www.ssobing.com/selleradmin/goods/regist')

    time.sleep(2)
    driver.get("http://www.ssobing.com/selleradmin/order/catalog")
    driver.maximize_window()

    selectall_btn = driver.find_elements_by_xpath("//span[@class='icon-check hand all-check']")

    start = '2018-09-01'
    end = '2018-10-26' #오늘 날짜로 fix

    #시작일을 2017-01-01로 설정, 마감일은 수집하는 날짜로 서버가 자동설정 해줌
    #input에 .send_keys가 아니라 value 값을 바꾸는 javascript를 실행해야 함
    collecting_date = driver.find_elements_by_xpath("//input[@name='regist_date[]']")
    driver.execute_script("arguments[0].setAttribute('value','2017-01-01')", collecting_date[0]) #변경가능

    selectall_btn[0].click() #Before 출고
    selectall_btn[1].click() #After 출고 이후

    start_collect_btn = driver.find_elements_by_xpath("//button[@type='submit']")
    start_collect_btn[0].click()

    time.sleep(3)

    #전체선택
    select_ops = driver.find_elements_by_xpath("//span[@class='custom-select-box-btn btn drop_multi_main']")
    select_ops[0].click()
    time.sleep(2)

    #양식선택
    #select_form = driver.find_element_by_xpath(//select[@id='select_down_35']")
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

def smartstore_download(id, pw):

    driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

    driver.get("https://sell.smartstore.naver.com/#/home/about")

    time.sleep(2)

    smart_login = driver.find_element_by_xpath("//a[@class='btn btn-primary']")
    smart_login.click()

    time.sleep(1)
    driver.get("https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2FnaverLoginCallback%3Furl%3Dhttps%253A%252F%252Fsell.smartstore.naver.com%252F%2523")
    time.sleep(1)

    input_id = driver.find_element_by_xpath("//input[@id='id']")
    input_pw = driver.find_element_by_xpath("//input[@id='pw']")
    input_id.send_keys(id)
    input_pw.send_keys(pw)

    time.sleep(2)
    login_btn = driver.find_element_by_xpath("//input[@class='btn_global']")
    login_btn.click()

    time.sleep(1)
    driver.get("https://sell.smartstore.naver.com/#/naverpay/manage/order")
    driver.maximize_window()

    #날짜선택 미구현

    driver.switch_to_frame("__naverpay")
    download_excel = driver.find_element_by_xpath("//button[@type='button'][@class='npay_btn_common size_medium type_basic btn_excel _click(nmp.seller_admin.order.manage.simple.excelDownload()) _stopDefault']")
    download_excel.click()

def street_download(id, pw):

    driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

    driver.get("https://login.11st.co.kr/login/Login.tmall?returnURL=http%3A%2F%2Fwww.11st.co.kr%2Fhtml%2Fmain.html&xfrom=")
    time.sleep(2)

    input_id = driver.find_element_by_xpath("//input[@id='loginName']")
    input_pw = driver.find_element_by_xpath("//input[@id='passWord']")

    input_id.send_keys(id)
    input_pw.send_keys(pw)

    login_btn = driver.find_element_by_xpath("//input[@class='btn_login']")
    login_btn.click()

    time.sleep(2)
    driver.get("http://soffice.11st.co.kr/Index.tmall")

    driver.get("https://soffice.11st.co.kr/escrow/SaleEndList.tmall")

    #날짜 선택 기능 미구현

    search_btn = driver.find_element_by_xpath("//button[@class='defbtn_lar ladtype defbtn_seh']")
    search_btn.click()
    time.sleep(2)

    excel_btn = driver.find_element_by_xpath("//a[@class='defbtn_lsm dtype6 btn_exceld']")
    excel_btn.click()

# 다운로드 실행부분
def perform_ssobing(request):
    ssobing_id = 'pineappleshop'
    ssobing_pw = 'joejoe11!!'
    ssobing_download(ssobing_id, ssobing_pw)

def perform_smartstore(request):
    smart_id = 'sk_baek0101'
    smart_pw = 'pineapple@_@_'
    smartstore_download(smart_id, smart_pw)

def perform_street(request):
    street_id = 'pineapples'
    street_pw = 'rudrud11!!'
    street_download(street_id, street_pw)

# 파일 선택 및 전송 부분

def send_all_files():
    pass