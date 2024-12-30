import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def initialize():
	load_dotenv()
	options = Options()
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--start-maximized")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
	wait = WebDriverWait(driver, 10)	
	return driver, wait

def login(driver, wait):
	driver.get("https://www.bigkinds.or.kr/v2/news/index.do")
	login_button = wait.until(
		EC.element_to_be_clickable((By.CSS_SELECTOR, "#header > div.hd-top > div > div.login-area > button.btn-login.login-modal-btn"))
	)
	login_button.click()

	login_id_input = wait.until(EC.presence_of_element_located((By.ID, "login-user-id")))
	login_id_input.send_keys(os.getenv('BIGKINDS_ID'))
	login_pwd_input = wait.until(EC.presence_of_element_located((By.ID, "login-user-password")))
	login_pwd_input.send_keys(os.getenv('BIGKINDS_PWD'))
	wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#login-btn"))).click()
	time.sleep(2)

def setting_search_option(driver, wait, or_keywords, required_keywords):
	# Select search tab
	driver.get("https://www.bigkinds.or.kr/v2/news/index.do")
	wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#srch-tab1"]'))).click()

	# Select date range
	date_element = wait.until(EC.element_to_be_clickable((By.ID, "date1-6")))
	date_element.find_element(By.XPATH, "..").click()

	# Select press tab and national daily newspapers
	wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#srch-tab2"]'))).click()
	press_element = wait.until(EC.element_to_be_clickable((By.ID, "전국일간지")))
	press_element.find_element(By.XPATH, "..").click()

	# Select detailed search tab
	wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.tab5"))).click()

	# Input search or_keywords
	keyword_input = wait.until(EC.presence_of_element_located((By.ID, "orKeyword1")))
	keyword_input.clear()
	keyword_input.send_keys(or_keywords)

	# Input search required keywords
	keyword_input = wait.until(EC.presence_of_element_located((By.ID, "exactKeyword1")))
	keyword_input.clear()
	keyword_input.send_keys(required_keywords)

	wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.news-search-btn"))).click()
	time.sleep(2)

	wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#collapse-step-3"))).click()
	time.sleep(5)

	download_button = wait.until(
		EC.element_to_be_clickable((By.CSS_SELECTOR, "#analytics-data-download > div.btm-btn-wrp > button"))
	)
	download_button.click()

def main():
    or_keywords = "살인, 살해, 숨지게, 숨져, 숨진, 방화, 불질러, 흉기, 둔기, 찔러, 목졸라, 납치, 감금, 폭행, 때려, 유기, 자살, 자해, 일가족, 가정불화, 부부싸움, 가정폭력, 데이트폭력, 교제폭력, 교제살인, 교제, 중상, 상해, 스토킹"
    required_keywords = ['여성', '여자', '아내', '부인', '전처', '동거녀', '내연녀', '애인', '여자친구', '여직원', '여학생']

    driver, wait = initialize()
    login(driver, wait)    
    try:
        for required_keyword in required_keywords:
            try:
                setting_search_option(driver, wait, or_keywords, required_keyword)
                print("브라우저가 열려 있습니다. 작업을 완료한 후 Enter를 눌러 다음 검색으로 넘어가세요.")
                input()
            except Exception as e:
                print(f"오류 발생: {e}")
                input()
            finally:
                continue
    finally:
        driver.quit()

if __name__ == "__main__":
	main()