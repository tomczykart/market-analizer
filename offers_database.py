import pandas as pd
from scrap_data import *


class BazaOfert:

    url = '''https://www.otodom.pl/pl/oferty/sprzedaz/dom/jozefow
            ?distanceRadius=0&page=1&limit=288&market=ALL&locations=%5Bcities_6-800%5D&
            buildingType=%5BDETACHED%5D&viewType=listing'''
    database_structure = ['link', 'name', 'price', 'price_per_meter', 'home_area', 'plot_area',
                        'parking', 'construct_year','construction_status']
    database_filename = 'baza_ofert.xlsx'

    def __init__(self):
        self.offers_database = pd.DataFrame(data=None, columns=BazaOfert.database_structure)
        self.update_database()

    def update_database(self):
        print('loading data to database...\n')
        self.append_data_to_database()
        print('downloading new offers...\n')
        self.merge_new_offers_to_database()
        print('checking new offers...\n')
        self.get_new_offers_details()
        print('saving database...\n')
        self.save_dataframe_to_excel(self.offers_database)

    def read_excel_to_dataframe(self, filename):
        try:
            data = pd.read_excel(filename, index_col=[0])
            return data
        except FileNotFoundError:
            print('No excel database found')
            data = pd.DataFrame(data=None)
            return data

    def append_data_to_database(self):
        data = self.read_excel_to_dataframe(BazaOfert.database_filename)
        self.offers_database = pd.concat([self.offers_database,data], ignore_index=True)

    def merge_new_offers_to_database(self):
        offers = self.scrap_offers()
        self.filtered_offers = self.find_new_offers(offers)
        self.offers_database = pd.merge(self.offers_database,self.filtered_offers, on='link', how='outer')

    def get_new_offers_details(self):
        for index in range(len(self.filtered_offers)):
            print(f'checking offer nr {index}...')
            link = self.filtered_offers.iloc[index,0]
            new_offer = Oferta(link)
            new_offer.get_offer_parameters()
            new_offer.add_parameters_to_offer(self.offers_database)


    def save_dataframe_to_excel(self, data):
        data.to_excel(BazaOfert.database_filename, sheet_name='Oferty domów')

    def scrap_offers(self):
        soup = get_site_html(BazaOfert.url)
        offers = offers_list(soup)
        return offers

    def find_new_offers(self, offers):
        db = self.offers_database
        filtered_offers = pd.Series(offers, name='link')
        filtered_offers = filtered_offers[filtered_offers.isin(db.link) == False]
        print(f'New offers: {len(filtered_offers)}\n')
        return filtered_offers


class Oferta(BazaOfert):

    def __init__(self,link):
        self.link = link
        self.name = self.link[33:-8]

    def get_offer_parameters(self):
        soup = get_site_html(self.link)
        offer_parameters = get_offer(soup)
        self.price = offer_parameters['price']
        self.price_per_meter = offer_parameters['price_per_meter']
        self.home_area = offer_parameters['home_area']
        self.plot_area = offer_parameters['plot_area']
        self.parking = offer_parameters['parking']
        self.construct_year = offer_parameters['construct_year']
        self.construction_status = offer_parameters['construction_status']

    def add_parameters_to_offer(self, db):
        db.loc[db['link'] == self.link] = [self.link, self.name, self.price, self.price_per_meter, self.home_area, self.plot_area, self.parking, self.construct_year, self.construction_status]









if __name__ == "__main__":
    Database = BazaOfert()
