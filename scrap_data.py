from selenium import webdriver

from msedge.selenium_tools import EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from bs4 import BeautifulSoup
import time
import sys

#website url with predefined search arguments
url = 'https://www.otodom.pl/pl/oferty/sprzedaz/dom/jozefow?distanceRadius=0&page=1&limit=288&market=ALL&locations=%5Bcities_6-800%5D&buildingType=%5BDETACHED%5D&viewType=listing'

#setup headless driver
options = EdgeOptions()
options.use_chromium = True
options.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
options.add_argument("--headless")
options.add_argument("disable-gpu")
driver = webdriver.Chrome(executable_path=r'C:\Users\atoma\OneDrive\Dokumenty\05-IT\5-edge-web-driver\msedgedriver', options = options)


#navigate to webpage
driver.get(url)

#get page html code
soup = BeautifulSoup(driver.page_source, 'html.parser')

#find offers on the page
offers = soup.findAll('a', {'class':'css-b2mfz3 es62z2j16'})

offers_links =  []
for offer in offers:
    link = offer["href"]
    offers_links.append(f'https://www.otodom.pl/{link}')
    print(link)



#stages of the construction to be searched for ('stan wykończenia'): 'w budowie', 'stan surowy otwarty', 'stan surowy zamknięty', 'do wykończenia'



#close driver
driver.close()
