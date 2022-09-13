# market-analizer

This program scraps webpage www.otodom.pl for an offers of houses under construction. Then it creates small database with offers of interests. Default region is Józefów, Masovian, Poland.

How to run the program:
1. It is a simple python script, just open terminal and run the script:
python offers_database.py
2. Script needs internet connection to run, you may be asked by windows firewall to give it permissions for access internet connection.
3. It usees Pandas, Selenium and BeautifulSoup. If you dont have this library error will rise.
4. At first run file may get a lot of offers to scrap. It will take some time. Script should write you the amount of new offers and the offer which is being checked.
5. At the very end the excel file will be saved in the same folder the script was executed. In the file there will be tabel with offers and relevant informations about them.
6. If u run the script again it will read data from excel first, so it will only add new offers if there will be any.
