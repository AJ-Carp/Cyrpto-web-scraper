from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import os
import time

def auto_crypto_pull():
    url = "https://coinmarketcap.com/currencies/bitcoin/?update=1719274192785"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features="html.parser")

    #retrieving "Bitcoin price" but removing price from the string 
    crypto_name = soup.find("span", title="Bitcoin").text
    crypto_name = crypto_name.replace("price", "")

    #retrieving price and removing $
    crypto_price = soup.find("span", class_ = "sc-d1ede7e3-0 fsQm base-text").text
    crypto_price = crypto_price.replace("$", "")

    #getting current date and time
    date_time = datetime.now()

    #creating dictionary of our price, name and time and adding it to a pandas table
    dict = {"Crypto Name" : crypto_name,
            "Price" : crypto_price,
            "Time Stamp" : date_time}
    df = pd.DataFrame([dict])

    #creating this table as a csv file (else) but if it already exists we are appending new data (if)
    if os.path.exists(r"/Users/ajcarpinello/Desktop/web scraping/Auto Crypto Web Scraper.csv"):
        df.to_csv(r"/Users/ajcarpinello/Desktop/web scraping/Auto Crypto Web Scraper.csv", mode = "a", header = False, index = False)
    else:
        df.to_csv(r"/Users/ajcarpinello/Desktop/web scraping/Auto Crypto Web Scraper.csv", index = False)

    print(df)

#running every 10 seconds
while True:
    auto_crypto_pull()  
    time.sleep(10)

