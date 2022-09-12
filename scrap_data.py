from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import EdgeOptions
from bs4 import BeautifulSoup
import numpy as np

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

def get_offer(soup):


    #filter data - construction status
    construction_status = soup.find('div', {'aria-label':'Stan wykończenia'})
    construction_status = construction_status.find('div', {'class':'css-1wi2w6s estckra5'})
    if construction_status is None:
        construction_status = np.nan
    else:
        construction_status = construction_status.text

    #filter data - area
    home_area = soup.find('div', {'aria-label':'Powierzchnia'})
    home_area = home_area.find('div', {'class':'css-1wi2w6s estckra5'})
    if home_area is None:
        home_area = np.nan
    else:
        home_area = home_area.text

    #filter data - plot area
    plot_area = soup.find('div', {'aria-label':'Powierzchnia działki'})
    plot_area = plot_area.find('div', {'class':'css-1wi2w6s estckra5'})
    if plot_area is None:
        plot_area = np.nan
    else:
        plot_area = plot_area.text

    #filter data - year of construction
    construct_year = soup.find('div', {'aria-label':'Rok budowy'})
    construct_year = construct_year.find('div', {'class':'css-1wi2w6s estckra5'})
    if construct_year is None:
        construct_year = np.nan
    else:
        construct_year = construct_year.text

    #filter data - parking
    parking = soup.find('div', {'aria-label':'Miejsce parkingowe'})
    parking = parking.find('div', {'class':'css-1wi2w6s estckra5'})
    if parking is None:
        parking = np.nan
    else:
        parking = parking.text

    #filter data - price
    price = soup.find('strong', {'aria-label':'Cena'})
    price = price.text

    #filter data - price
    price_per_meter = soup.find('div', {'aria-label':'Cena za metr kwadratowy'})
    price_per_meter = price_per_meter.text

    #create dictionary for an offer
    offer = {'home_area':home_area, 'plot_area':plot_area, 'construct_year':construct_year, 'parking':parking, 'price':price, 'price_per_meter':price_per_meter, 'construction_status':construction_status}

    return offer


#website url with predefined search arguments
#url = 'https://www.otodom.pl/pl/oferty/sprzedaz/dom/jozefow?distanceRadius=0&page=1&limit=288&market=ALL&locations=%5Bcities_6-800%5D&buildingType=%5BDETACHED%5D&viewType=listing'

#soup = get_site_html(url)
#offers = offers_list(soup)
#offer_to_check = get_site_html(offers[13])
#offers_verification = check_offer(offer_to_check)
#offer_parameters = get_offer(offer_to_check)
#print(offer_parameters)
