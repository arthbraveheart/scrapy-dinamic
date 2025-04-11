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
from tools import load_pkl
from settings import out_path

# Suppress all warnings
warnings.filterwarnings("ignore")

today = time.strftime("%d-%m-%Y")

search = load_pkl('search').loc[:, 'Madeira'].to_list()

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

with open(str(out_path) + f"Prices_Madeira_{today}.csv", "w", newline="", encoding="utf-8-sig") as f:
    csv_writer = csv.writer(f, delimiter=';')
    titulo = ['Name', 'Price', 'URL']
    csv_writer.writerow(titulo)

    for url in search:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        elements = soup.find_all('div', {'class': 'cav--c-gqwkJN cav--c-gqwkJN-knmidH-justifyContent-spaceBetween cav--c-gqwkJN-ieFWNPI-css'})
        try:
            for element in elements:
                name, price = get_things_done(element)
                linha = [name, price, url]
                print(linha)
                csv_writer.writerow(linha)
        except:
            linha = ['empty', 0, url]
            print(linha)
            csv_writer.writerow(linha)

time2 = time.time()
print("\nExecution time:", time2 - time1)
driver.quit()