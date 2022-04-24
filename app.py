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

def get_leiden_pararius_page_source(page_number: int):
    url = f'https://www.pararius.nl/huurwoningen/leiden/900-1500/page-{page_number}'
    options = Options()
    options.add_argument(f"window-size={1920},{1080}")
    options.add_argument("--disable-notifications")
    options.add_argument("disable-infobars")
    # download latest webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    time.sleep(10)
    return driver.page_source

#
def handler(event, context):

    page_source = get_leiden_pararius_page_source(1)
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(
            {'page_source': page_source}
        )
    }
