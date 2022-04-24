from dataclasses import dataclass
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import functools
import json

headers = {
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}

# def get_leiden_pararius_page_source(page_number: int):
#     url = f'https://www.pararius.nl/huurwoningen/leiden/900-1500/page-{page_number}'
#     options = Options()
#     options.add_argument(f"window-size={1920},{1080}")
#     options.add_argument("--disable-notifications")
#     options.add_argument("disable-infobars")
#     # download latest webdriver
#     driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#     driver.get(url)
#     time.sleep(10)
#     return driver.page_source

def get_leiden_pararius_page_source(page_number: int):
    url = f'https://www.pararius.nl/huurwoningen/leiden/900-1500/page-{page_number}'
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/stable/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("window-size=2560x1440")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    
    driver = webdriver.Chrome("/opt/chromedriver/stable/chromedriver", options=chrome_options)
    driver.get(url)
    time.sleep(10)
    
    return driver.page_source

def handler(event, context):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/stable/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("window-size=2560x1440")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome = webdriver.Chrome("/opt/chromedriver/stable/chromedriver", options=chrome_options)
    chrome.get("https://cloudbytes.dev")
    
    page_source = chrome.find_element_by_xpath("//html").text
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(
            {'page_source': page_source}
        )
    }
