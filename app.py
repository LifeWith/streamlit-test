import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")

# st.write('test')
URL = st.text_input('로그인 할 주소를 입력하세요.')
SHOP_CODE = st.text_input('로그인 할 샵코드를 입력하세요.')
ID = st.text_input('로그인할 아이디를 입력하세요.')
PWD = st.text_input('로그인할 비밀번호를 입력하세요')

def Login(driver, url, shopCode, id, pwd):
    try:
        # 칵테일 접속
        driver.get(url)

        # 1초 대기
        time.sleep(1)

        # 계정 입력
        elem = driver.find_element(By.ID, "strShopCode")
        elem.clear()
        elem.send_keys(shopCode)

        elem = driver.find_element(By.ID, "strId")
        elem.clear()
        elem.send_keys(id)

        elem = driver.find_element(By.ID, "strPass")
        elem.clear()
        elem.send_keys(pwd)

        elem = driver.find_element(By.CLASS_NAME, "loginBT_c")
        elem.click()

    except Exception as e:
        st.write(e)
        
def Run():
  with webdriver.Chrome(options=options) as driver: 
    Login(driver, URL, SHOP_CODE, ID, PWD)
    st.write(driver.current_url)
    
if st.button('TEST'):
  Run()
