# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:45:27 2024

@author: Mucho
"""

from selenium import webdriver
import csv
import time
import re
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import warnings
from tools import load_pkl
from settings import  out_path

# Suppress all warnings
warnings.filterwarnings("ignore")

today  = time.strftime("%d-%m-%Y")

search = load_pkl('dular_links').loc[:,['SKU','Cód PAI','Magalu']]


options = Options()
#options.add_argument("--headless")
prefs = {"profile.managed_default_content_settings.images":2,
    "profile.default_content_setting_values.notifications":2,
    "profile.managed_default_content_settings.stylesheets":2,
    #"profile.managed_default_content_settings.cookies":2,
    #"profile.managed_default_content_settings.javascript":1,
    #"profile.managed_default_content_settings.plugins":1,
    "profile.managed_default_content_settings.popups":2,
    #"profile.managed_default_content_settings.geolocation":2,
    #"profile.managed_default_content_settings.media_stream":2,


    }
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(options=options)#Firefox()

def get_things_done(element):
    
    try:
    
        json_loads = element.text
        pattern_price   = re.compile(r'"price":"(\d+\.\d{2}|\d+)"') #testar sem casa decimal
        pattern_name   = re.compile(r'"name":"(.*?)"')
        prices = re.findall(pattern_price, json_loads)
        names  = re.findall(pattern_name, json_loads)
        return names, prices
   
    except:
        print("****************** Fail to get PRICE *******************")
        return ['empty'],['empty']

time1 = time.time()

# Cria o arquivo CSV
with open(out_path + f"Prices_Magalu_{today}.csv", "w", newline="", encoding="utf-8-sig") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
   
    titulo = ['SKU','Cód PAI','Name', 'Price', 'URL',]
    csv_writer.writerow(titulo)
    
    for i,row in search.iterrows():
        
        driver.get(row['Magalu'])
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        element = soup.find('script',{'type':'application/ld+json'})
        names, prices = get_things_done(element)
        for name, price in zip(names,prices):
            if name!='empty':
                linha = [row['SKU'],row['Cód PAI'],name, price.replace('.',','), row['Magalu']]
                print(linha)
                csv_writer.writerow(linha)
            else:
                continue
    
    
time2 = time.time()    
print("\nExecution time:",time2-time1) 
driver.close()    
    
    
    
    
    
    
    
    

        