import time, datetime
import requests
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
URL = st.text_input('로그인 할 주소를 입력하세요.(끝에 / 빼고)')
SHOP_CODE = st.text_input('로그인 할 샵코드를 입력하세요.')
ID = st.text_input('로그인할 아이디를 입력하세요.')
PWD = st.text_input('로그인할 비밀번호를 입력하세요')
HOOK = st.text_input('알림 받을 슬랙 채널 hook 주소를 입력하세요.')

START_BUTTON = st.button('테스트 start')
STOP_BUTTON = st.button('테스트 stop(대기시간 지나고 다음 순번에 중단됨)')
RUN = True

def send_msg(title:str):
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    message = '[' + nowDatetime + '] ' + title
    response = requests.post(
        HOOK,  
        headers={
        'content-type': 'application/json'
        },
        json={
        'text': title,
        'blocks': [
            {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': message
            }
            }
        ]
        }
    )

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)


def Login(driver, url, shopCode, id, pwd, cnt:int):
    try:
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
        
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        if driver.current_url == URL + '/CRM.LoadPage':
            st.write('[' + nowDatetime + '] 로그인 성공-' + str(cnt))
            if cnt%10 == 1:
                send_msg('로그인 성공-' + str(cnt))
        else:
            st.write('[' + nowDatetime + '] 로그인 실패' )
            send_msg('로그인 실패')

    except Exception as e:
        st.write(e)
        send_msg('Exception 발생')

def ValidCheck():
    if URL == '':
        st.write('URL을 입력하세요.')
        return False
    elif SHOP_CODE == '':
        st.write('샵코드를 입력하세요.')
        return False
    elif ID == '':
        st.write('ID를 입력하세요.')
        return False
    elif PWD == '':
        st.write('비밀번호를 입력하세요.')
        return False
    elif HOOK == '':
        st.write('HOOK 주소를 입력하세요.')
        return False
    else:
        return True        
        
        
def Run():
  with webdriver.Chrome(options=options) as driver: 
    
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    st.write('[' + nowDatetime + '] 로그인 테스트 start')
    send_msg('로그인 테스트 start')

    count = 0
    wait = 60 # 초단위
    while RUN == True:
        if count > 0:
            time.sleep(wait)
        count = int(count) + 1
        Login(driver, URL, SHOP_CODE, ID, PWD, count)

    st.write('[' + nowDatetime + '] 로그인 테스트 stop')
    send_msg('로그인 테스트 stop')
    
    

if START_BUTTON:
    if ValidCheck():
        RUN = True
        Run()

if STOP_BUTTON:
    RUN = False
    st.write('STOP_BUTTON')
    send_msg('STOP_BUTTON')        
