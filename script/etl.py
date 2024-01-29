from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import sqlite3


class CheeseScrapping():
    
    def __init__(self, url):
        self.url = url
    
    def extract(self):
        data = urlopen(self.url)
        data = data.read()
        return BeautifulSoup(data)
    
    def transform(self, soup):
        tds = soup.find_all('td')
        tds_url = [td.find('a') for td in tds if td.find('strong') is None and td.text != '\xa0']
        tds_url = [td['href'] if td is not None else None for td in tds_url]
        tds = [td.text.strip() for td in tds if td.find('strong') is None and td.text != '\xa0']
        
        cheeses = tds[0::3]
        families = tds[1::3]
        doughs = tds[2::3]
        urls = tds_url[0::3]

        return pd.DataFrame({'cheeses': cheeses, 'families': families, 'doughs': doughs, 'urls':urls})
    
    def load(self, db_path, table, dataframe):
        
        sqlite_connection = sqlite3.connect(db_path)
        dataframe.to_sql(table, con=sqlite_connection, index=False, if_exists='replace')
        dataframe['update_date'] = pd.Timestamp.now()
        sqlite_connection.close()
        
        return dataframe
        