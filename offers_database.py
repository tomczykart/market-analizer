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
        #BazaOfert.new_offers = pd.DataFrame(self.scrap_offers())
        #BazaOfert.new_offers.columns = ['link']
        #BazaOfert.new_offers.set_index('link')
        #BazaOfert.offers_database = pd.read_excel('offers.xlsx')
        #BazaOfert.offers_database.set_index('link')
        #BazaOfert.offers_database_archive = pd.read_excel('offers_archive.xlsx')
        #BazaOfert.offers_database_archive.set_index('link')

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

    def save_dataframe_to_excel(self, data):
        data.to_excel(BazaOfert.database_filename, sheet_name='Oferty domów')

    def scrap_offers(self):
        soup = get_site_html(BazaOfert.url)
        offers = offers_list(soup)
        return offers

    def find_new_offers(self, offers):
        db = self.offers_database
        new_offers = pd.Series(offers)
        new_offers = new_offers[new_offers.isin(db.link) == False]
        return new_offers

    def update_database(self):
        self.append_data_to_database()
        self.save_dataframe_to_excel(self.offers_database)





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
        BazaOfert.offers_database = BazaOfert.offers_database.assign(expired = ~BazaOfert.offers_database.index.isin(BazaOfert.new_offers))
        self.expired_offers = BazaOfert.offers_database.loc[BazaOfert.offers_database['expired']==False]
        print(f'Baza ofert z archiwalnymi = {BazaOfert.offers_database}')
        print(f'oferty przedawnione = {self.expired_offers}')




class Oferta(BazaOfert):

    def __init__(self, link, name, price, home_area, plot_area):
        self.link = link
        self.name = name
        self.price = price
        self.home_area = home_area
        self.plot_area = plot_area

if __name__ == "__main__":
    Database = BazaOfert()




#Database.check_if_in_archive()
#Database.check_if_in_database()
#Database.add_new_offers()
#Database.archive_old_offers()
#Database.save_excel()
