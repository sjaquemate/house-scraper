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

def get_headless_aws_lambda_driver():
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
    return driver 

def get_local_chrome_driver():
    options = Options()
    options.add_argument(f"window-size={1920},{1080}")
    options.add_argument("--disable-notifications")
    options.add_argument("disable-infobars")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver

def get_leiden_pararius_page_source(page_number: int, 
                                    get_driver_func=get_headless_aws_lambda_driver):
    url = f'https://www.pararius.nl/huurwoningen/leiden/900-1500/page-{page_number}'
    
    driver = get_driver_func()
    driver.get(url)
    time.sleep(10)
    
    return driver.page_source

def handler(event, context):

    page_source = get_leiden_pararius_page_source(1)
        
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(
            {'page_source': page_source}
        )
    }
