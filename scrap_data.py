from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import EdgeOptions
from bs4 import BeautifulSoup

#setup headless driver
options = EdgeOptions()
options.use_chromium = True
options.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("disable-gpu")

def get_site_html(url):
    #setup driver
    driver = webdriver.Chrome(executable_path=r'C:\Users\atoma\OneDrive\Dokumenty\05-IT\5-edge-web-driver\msedgedriver', options = options)

    #navigate to webpage
    driver.get(url)

    #get page html code
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #close driver
    driver.close()

    return soup


def offers_list(soup):

    #find offers on the page
    offers = soup.findAll('a', {'class':'css-b2mfz3 es62z2j16'})

    #create a list of offers
    offers_links =  []
    for offer in offers:
        link = offer["href"]
        offers_links.append(f'https://www.otodom.pl/{link}')

    #remove duplicates because of recommended offers
    offers_links = set(offers_links)
    offers_links = list(offers_links)

    return offers_links

def check_offer(soup):

    #filter data - construction status
    construction_status = soup.find('div', {'aria-label':'Stan wykończenia'})
    construction_status = construction_status.find('div', {'class':'css-1wi2w6s estckra5'})
    print(construction_status.text)
    return construction_status.text

def get_offer(soup):

    #filter data - area
    area = soup.find('div', {'aria-label':'Powierzchnia'})
    area = area.find('div', {'class':'css-1wi2w6s estckra5'})
    area = area.text

    #filter data - plot area
    plot_area = soup.find('div', {'aria-label':'Powierzchnia działki'})
    plot_area = plot_area.find('div', {'class':'css-1wi2w6s estckra5'})
    plot_area = plot_area.text

    #filter data - year of construction
    construct_year = soup.find('div', {'aria-label':'Rok budowy'})
    construct_year = construct_year.find('div', {'class':'css-1wi2w6s estckra5'})
    construct_year = construct_year.text

    #filter data - parking
    parking = soup.find('div', {'aria-label':'Miejsce parkingowe'})
    parking = parking.find('div', {'class':'css-1wi2w6s estckra5'})
    parking = parking.text

    #filter data - price
    price = soup.find('strong', {'aria-label':'Cena'})
    price = price.text

    #filter data - price
    price_per_meter = soup.find('div', {'aria-label':'Cena za metr kwadratowy'})
    price_per_meter = price_per_meter.text

    #create dictionary for an offer
    offer = {'Area':area, 'Plot area':plot_area, 'Construction year':construct_year, 'Parking':parking, 'Price':price, 'Price per meter':price_per_meter}

    return offer


#website url with predefined search arguments
url = 'https://www.otodom.pl/pl/oferty/sprzedaz/dom/jozefow?distanceRadius=0&page=1&limit=288&market=ALL&locations=%5Bcities_6-800%5D&buildingType=%5BDETACHED%5D&viewType=listing'

soup = get_site_html(url)
offers = offers_list(soup)
offer_to_check = get_site_html(offers[13])
offers_verification = check_offer(offer_to_check)
offer_parameters = get_offer(offer_to_check)
