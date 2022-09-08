import pandas as pd
from scrap_data import *


class BazaOfert:

    url = 'https://www.otodom.pl/pl/oferty/sprzedaz/dom/jozefow?distanceRadius=0&page=1&limit=288&market=ALL&locations=%5Bcities_6-800%5D&buildingType=%5BDETACHED%5D&viewType=listing'
    offers_database = {}
    offers_database_archive = {}
    new_offers = {}

    def __init__(self):
        BazaOfert.new_offers = pd.DataFrame(self.scrap_offers())
        BazaOfert.new_offers.columns = ['link']
        BazaOfert.new_offers.set_index('link')
        BazaOfert.offers_database = pd.read_excel('offers.xlsx')
        BazaOfert.offers_database.set_index('link')
        BazaOfert.offers_database_archive = pd.read_excel('offers_archive.xlsx')
        BazaOfert.offers_database_archive.set_index('link')

    def scrap_offers(self):
        soup = get_site_html(BazaOfert.url)
        offers = offers_list(soup)
        return offers

    def show_data(self):
        print(BazaOfert.new_offers)

    def check_if_in_archive(self):
        BazaOfert.new_offers = BazaOfert.new_offers.assign(already_exists = BazaOfert.new_offers.index.isin(BazaOfert.offers_database_archive.index))
        BazaOfert.new_offers = BazaOfert.new_offers.loc[BazaOfert.new_offers['already_exists']==False]

    def check_if_in_database(self):
        BazaOfert.new_offers = BazaOfert.new_offers.assign(already_exists = BazaOfert.new_offers.index.isin(BazaOfert.offers_database.index))
        self.new_unregistered_offers = BazaOfert.new_offers.loc[BazaOfert.new_offers['already_exists']==False]
        print(f'Nowe oferty:{self.new_unregistered_offers}')

    def add_new_offers(self):
        BazaOfert.offers_database = BazaOfert.offers_database.merge(self.new_unregistered_offers, on='link', how='outer')

    def archive_old_offers(self):
        pass

    def save_excel(self):
        BazaOfert.offers_database.to_excel('offers.xlsx',sheet_name='Oferty aktualne')
        BazaOfert.offers_database_archive.to_excel('offers_archive.xlsx',sheet_name='Oferty archiwalne')


class Oferta(BazaOfert):

    def __init__(self, link, name, price, home_area, plot_area):
        self.link = link
        self.name = name
        self.price = price
        self.home_area = home_area
        self.plot_area = plot_area

Database = BazaOfert()
Database.show_data()
Database.check_if_in_archive()
Database.check_if_in_database()
Database.add_new_offers()
Database.save_excel()
