# -*- coding: utf-8 -*-
"""
Modified for Docker compatibility
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import re
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import warnings
from sqlalchemy import text,create_engine, Column, Integer, String, Numeric, Text, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from contextlib import closing
from urllib.parse import urlencode, quote

Base = declarative_base()

DATABASE_URI = "postgresql://scrapy:scrapy@db:5432/scrapy"

class Core_Model(Base):
    __tablename__ = 'core'
    #__table_args__ = {'schema': 'public'}  # Remove if not using schemas

    id = Column(Integer, primary_key=True, autoincrement=True)
    seller = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    url = Column(Text, nullable=False)
    ean = Column(BigInteger, nullable=False)  # Matches BIGINT in SQL
    date_now = Column(DateTime, server_default=func.now())  # Database handles default

# Suppress all warnings
warnings.filterwarnings("ignore")

today = time.strftime("%d-%m-%Y")
base_url = 'https://www.madeiramadeira.com.br/busca'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
#Base.metadata.create_all(self.engine)

#search = load_pkl('search').loc[:, 'Madeira'].to_list()

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.default_content_setting_values.notifications": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
    "profile.managed_default_content_settings.popups": 2,
}
options.add_experimental_option("prefs", prefs)

# Auto-install ChromeDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

def get_things_done(element):
    try:
        json_loads = element.text
        pattern_price = re.compile(r'R\$(\d+\.\d+\,\d{2}|\d+\,\d{2}|\d+)')
        pattern_name = re.compile(r'(.*?)R\$')
        prices = re.findall(pattern_price, json_loads)[0]
        names = re.findall(pattern_name, json_loads)[0]
        return names, prices
    except:
        print("****************** Fail to get PRICE *******************")
        return 'empty', 0

time1 = time.time()


with closing(engine.connect()) as conn:
    result = conn.execution_options(stream_results=True).execute(
        text("""SELECT description,ean FROM "dular_eans" """)
    )

    for row in result:
        ean = row[1]
        product_name = str(row[0]).strip()
        params = {'q': product_name}
        encoded_query = quote(product_name)
        url = f"{base_url}?q={encoded_query}"
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        elements = soup.find_all('div', {
            'class': 'cav--c-gqwkJN cav--c-gqwkJN-knmidH-justifyContent-spaceBetween cav--c-gqwkJN-ieFWNPI-css'})
        counter_elements = 0
        try:
            for element in elements:
                if counter_elements != 3:
                    name, price = get_things_done(element)
                    linha = [name, price, url]
                    print(linha)
                    #csv_writer.writerow(linha)
                    record = Core_Model(
                        seller='Madeira Madeira',
                        name=name,
                        price=float(price.replace('R$', '').replace('.', '').replace(',', '.').strip()),
                        url=url,
                        ean=ean,
                        # date_now=item['date_now']
                    )
                    session.add(record)
                    session.commit()
                    counter_elements += 1
                else:
                    break
        except:
            linha = ['empty', 0, url]
            print(linha)
            #csv_writer.writerow(linha)

time2 = time.time()
print("\nExecution time:", time2 - time1)
driver.quit()
session.close()