# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "001FBFE4B164B79A28E5670C85089B9BC39DB87AD9898F551083D5A70ED46F29DC1F01A3A6E58DEAE4C2FED8EEC20785CFEBFFD5431AB00C708944B5E2526BAD43508FD4176D9E4EFAEE14B28AD508B77FC159A94DF307E7808B8C13F3655F9EEAE622574176D040311E00A1F257DCD34550F2DD5285198C69C1F4D495F42B6B0A2F64D09BFD709D0DB787B526DC029FF13692AA3C6BC78B07CAE3FFC38D68A52914E4E9115343315CF6AB766C7E549E1EA31332BB38F4BBFCE8AF7F17002FA7514E374ABF1181F2CFCD5C1BA264AC8540E9803CB0F1DEF2B9CB8D624D47679F2E69C3B9F283A83EF996BBB570DC8AA2893642EB728B1774B4ABAC01DCF4629B2CA282F74CCC8A1BB58495D0CF3956553C252A4A4E382A738F46A11DE680E32D27FA48E76FD124E3CF3D0023A9A2901D1B23459D28A4776DDA15D9DB76CEFCFEF6E5B0D04B93F3C8D47179A054504459B41508616EB5BCA5BA0BEAACC79E6CF454"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
