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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DBF1BA1714BE9539DE1A4422C567AA1DCDFB5A02527321D00CFD1B768AA709A0F2A906CD41B6E0060321CB8877F6955186CF6DAD4DE4473EF53675510479B6F47AEE0BEB54E27822CC6D8304FE4E198205828ED59A584A233BD11DBF97FFEC58D395ADFD084D75351D47A6B8C796A64331940B1A2F0E6FFAF6E8D94D9ECE69C915179053579CA205B17301CC27F8976FBCB3C5C7DF1B7131C27D7658128D2FD55FC7EB7BA6CB2C834B9FF312B38685716EC0FA4C1918E1AFBBCA2459E8B2136AD4FE7A55315AE6FC497176BC9E6E2CDBA8956761C7CE21757376BB7E9C49DF14E476BBCD8A4610CA0C968CD12756204C2E0E6458D7F58681BC19D0579ADFC582B3E16A1DF8630E6B6C215F2661CAC80057AA40DB9FF36F49F161080B700B0FBF76C2A0B365B785E438D51782776359C55CDD7A3D38C8BB86BBE848B0E39FCDCF9BE335325E882B1969A31C11C59ABD735C113AD5BB7969F376DB35AD34AF6AF3"})
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
