from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time 
from tables.houses import House
from datetime import datetime 

def get_local_chrome_driver():
    options = Options()
    options.add_argument(f"window-size={1920},{1080}")
    options.add_argument("--disable-notifications")
    options.add_argument("disable-infobars")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver

def get_pararius_houses_from_page_source(page_source) -> list[House]:

    b = BeautifulSoup(page_source)
        
    houses_li_list = b.find_all("li", class_="search-list__item search-list__item--listing")  

    houses = []
    for house_li in houses_li_list:

        a_list = house_li.find_all("a")
        a_image = a_list[0]
        a_page = a_list[1]
        a_makelaar = a_list[2]
        
        makelaar = ''.join(a_makelaar.contents)
        name = ''.join(a_page.contents)
        link = 'https://www.pararius.nl' + a_page['href']
        div_price = house_li.find_all("div", class_="listing-search-item__price")[0]
        price = ''.join(div_price.contents).strip()
        
        house = House(name=name, price=price, link=link, makelaar=makelaar, timestamp=datetime.now())
        houses.append(house)

    return houses

class ParariusScraper:
    
    
    def __init__(self) -> None:
        self.driver = get_local_chrome_driver()
        
    def get_leiden_pararius_page_source(self, page_number: int) -> str:
        url = f'https://www.pararius.nl/huurwoningen/leiden/900-1700/page-{page_number}'

        self.driver.get(url)
        time.sleep(10)

        return self.driver.page_source

    def scrape(self) -> list[House]:
        page_number = 1
        houses = []
        while True:
            page_source = self.get_leiden_pararius_page_source(page_number)
            new_houses = get_pararius_houses_from_page_source(page_source)
            if len(new_houses) == 0:
                break
            houses += new_houses 
            page_number += 1 
        
        return houses
