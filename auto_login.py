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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F30DB378D2C50BD91F90B03472F843DA3366B5BE098A7921D2E488951ED3B9F5D93A55E89024894AB20008B54603677F34D8F320BB330F1E615D3C0C89001C094B2AB196E3F0EF705788A32478108F4A5C6484EBCEE387F70A0AFD60689C41B0624B020451F60567D034D19C22CBD9BD9033DB9E1D7DACF777C0026FD354DCD556705A5243B61A83159CD9D85DB06AE03B6B33086A929517FBC03068D9F3074A868B2E58A2DEAC1D169AA8BC2CC647B36B7136778A1CA7BD7A6A7B812FF95F95FB0E81FDB45224231EED9D80096557196236D210EA558017C63EDD7B1303FD97290FB66B383DAA7F2541EB5DD4B669EFE624DEEACC9C8678C713ED7C50F6E55332ADE56686C5E029D5E70CC5A55687B6095DB20010D5612FF5D744DFAB2DDECCAEFF0CAD983891C4865B04896B1F97D12C3C0D5ABA3609ABA32E2545DF6D5093008025F09AC4362C0CF46EDA76C4AF6F7DA0491362145AF337274D1E0E4DE7B7"})
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
