# import spacy
# import en_core_web_sm
# nlp = en_core_web_sm.load()

import requests
import re
from bs4 import BeautifulSoup, element
import time
import pandas as pd
import random
import csv
import sys
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.db import *
from ecig_parsing import *


BASE = 'https://www.myvaporstore.com' 
SITE = MY_VAPOR_STORE

links = [  
      '/Disposable-Vapes-s/885.htm',
    '/Disposables-Prefilled-Carts-s/1116.htm',
    '/Sale-Disposables-s/1134.htm',
    '/Best-Selling-Ejuice-s/1163.htm', '/Best-Selling-Ejuice-s/1163.htm', 
    '/Best-Selling-Ejuice-s/1163.htm', '/Naked-100-E-Liquid-s/447.htm', 
    '/Freebase-E-liquids-s/1062.htm', '/Nicotine-Salt-Eliquid-s/633.htm', 
    '/Apple-Flavored-eLiquid-s/299.htm', '/Bakery-and-Desserts-eLiquid-s/291.htm', '/Banana-Flavored-eLiquid-s/301.htm', '/Berries-Flavored-eLiquid-s/302.htm', '/Caramel-eLiquid-s/310.htm', '/SearchResults.asp?Search=cereal', '/Cherry-Flavored-eLiquid-s/300.htm', '/Chocolate-eLiquid-s/306.htm', '/Cinnamon-eLiquid-s/308.htm', '/Citrus-Flavored-eLiquid-s/297.htm', '/Coconut-Flavored-eLiquid-s/295.htm', '/Coffee-and-Tea-eLiquid-s/292.htm', '/Custards-and-Creams-eLiquid-s/293.htm', '/Freebase-E-liquids-s/1062.htm', '/Fruit-eLiquid-s/307.htm', '/Grape-Flavored-eLiquid-s/303.htm', '/Lemonade-eLiquid-Flavors-s/570.htm', '/Mango-Flavored-eLiquid-s/304.htm', '/Melons-Flavored-eLiquid-s/298.htm', '/Menthol-Mint-Flavors-eLiquid-s/54.htm', '/Nicotine-Salt-Eliquid-s/633.htm', '/Peach-Flavored-eLiquid-s/305.htm', '/Strawberry-Flavor-eLiquid-s/294.htm', '/Tobacco-Flavors-eLiquid-s/53.htm', '/Tobacco-Free-Nicotine-s/1022.htm', '/Vanilla-eLiquid-s/309.htm', '/Watermelon-Flavored-eLiquid-s/296.htm', 
    '/eLiquids-by-Flavor-s/290.htm',
    '/sale-eliquids-s/1133.htm',
    '/Box-Mod-Ecig-Starter-Kits-s/523.htm',
    '/Pen-Style-Ecig-Starter-Kits-s/524.htm',
    '/Pod-Systems-Ecig-Starter-Kits-s/525.htm',
    '/E-Cig-Starter-Kits-E-Cigarette-s/70.htm', 
    '/Vape-Brands-Aspire-s/155.htm', '/Digiflavor-Ecig-Tanks-s/569.htm', 
    '/category-s/1074.htm', '/Efest-Batteries-and-Chargers-s/340.htm', 
    '/iSmoka-Eleaf-iStick-Box-Mod-s/224.htm', 
    '/FreeMax-Ecig-Products-s/683.htm', '/GeekVape-s/406.htm',
      '/Hamilton-Devices-s/1026.htm', '/E-Cigarette-Brands-Innokin-s/135.htm', 
      '/Joyetech-E-Cig-Brands-s/138.htm', '/Kangertech-E-Cigarettes-s/143.htm', 
      '/E-Cig-Brands-OVNS-s/666.htm', '/RELX-Ecig-Products-s/941.htm', 
      '/SMOK-VAPES-and-Accessories-s/159.htm', '/Suorin-Ecig-Products-s/583.htm',
        '/Tyson-Disposables-s/1148.htm', '/UWELL-Crown-Ecig-Tanks-and-Mods-s/374.htm',
          '/Vandy-Vape-Ecig-RDA-and-RTA-s/532.htm', '/Vaporesso-s/424.htm',
            '/Voopoo-Ecig-Mods-s/552.htm', '/Yocan-s/663.htm', 
            '/Yocan-Products-s/673.htm', '/E-Cig-Brands-iJoy-s/471.htm',
    '/Shop-by-Brand-s/194.htm', 
        '/Hemp-Vape-Kits-s/1184.htm', 
    '/Hemp-Disposables-s/1182.htm', 
    '/Hemp-Edibles-Rolls-s/1183.htm', 
    '/Alternative-Glass-Pipes-Bubblers-s/1115.htm', 
    '/Hemp-Accessories-s/1186.htm', 
    '/Hemp-Cartridges-Pods-s/1185.htm', 
    '/Dry-Herb-Oil-Wax-Vaporizer-s/621.htm', 
    '/Vape-Tanks-E-Cigarette-s/65.htm',
    '/official-myvaporstore-apparel-s/357.htm',
    '/Batteries-E-Cigarette-s/24.htm',
    '/Battery-Cases-E-Cigarette-s/548.htm',
    '/Bottles-E-Cigarette-s/25.htm',
    '/ECig-Chargers-s/221.htm',
    '/Drip-Tips-E-Cigarette-s/68.htm',
    '/Miscellaneous-s/29.htm',
    '/Replacement-Coils-and-pod-cartridges-s/163.htm',
    '/thread-adapters-for-ecig-s/60.htm',
    '/sale-Hardware-s/1140.htm',
    '/Sale-Herbal-Alternative-Products-s/1145.htm',
    '/Wick-Wire-s/164.htm',
    '/Accessories-s/207.htm', 
    '/New-Arrivals-Vape-s/77.htm', 
    '/Vape-Clearance-Sale-s/398.htm'
]


print('TOTAL LINKS', len(links))
found = dict()


def get_html(url, timeout=5):  # Added timeout parameter


    driver = None
    html = ''
    simple = ''
    try:
        res = requests.get(url)
        simple = res.text
        options = Options()
        options.add_argument('--headless')
        options.page_load_strategy = 'eager'

        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(5)
        driver.get(url)

        # Robust explicit wait: Wait for multiple elements or a specific element to be visible
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'body'))
        )
        time.sleep(2) #add a small sleep to ensure any javascript has finished.

        html = driver.page_source

    except Exception as ex:
        print(f"An error occurred: {ex}")
        html = simple

    finally:
        if driver:
            html = driver.page_source
            driver.quit()

    return simple, html

if __name__ == "__main__":
    from collections import Counter

    product_list = list()
    all_headers = list()
    header_counter = Counter(all_headers)
    header_samples = dict()
    
    has_header = False
    
    with open(f'scraping/data-latest/{SITE}_scrape.csv', mode='w') as file:

        for l in links:
            page = 1
            site_section = l.split('/')[1].split('-s')[0]  # Extract section name


            while True:
                url = f'{BASE}{l}??categoryIds=null&page={page}#product-grid'
                print(url)

                if url in found:
                    reqtxt = found[url]
                else:
                    simpletxt, reqtxt = get_html(url)
                    found[url] = reqtxt
                #reqtxt = get_html(url)
                soup = BeautifulSoup(reqtxt)
                products = soup.find_all('div', {'class': 'pa2 w-100 pt2 ph2 pb3 ph3-ns pb4-ns tl'})
                print(url, len(products))
                
                if len(products) == 0:
                    break
                page += 1

                for product_card in products:
                    if not isinstance(product_card, element.Tag):
                        continue

                    product_info = {}

                    # Extract href
                    link_tag = product_card.find('a', class_='relative db w-100 _tj74vx', href=True)
                    if link_tag:
                        href = link_tag['href']
                        link = f'{BASE}{href}'
                        product_info['link'] = link
                        

                    # Extract product name
                    name_tag = product_card.find('h4', class_='mv0', attrs={'data-clicktarget': 'colorProductName'})
                    if name_tag:
                        product_info['title'] = name_tag.text.strip()

                    # Extract brand
                    brand_div = product_card.find('div', class_='_uka9f1', attrs={'data-brand': True})
                    if brand_div:
                        product_info['brand'] = brand_div.text.strip()

                    # Extract base price
                    base_price_div = product_card.find('div', class_='pv1 _11o35w1 _uxrrysc', attrs={'data-product-base-price': True})
                    if base_price_div:
                        product_info['regular_price'] = base_price_div.text.strip()

                    # Extract sale price
                    sale_price_span = product_card.find('span', class_='_dqivtj', attrs={'data-clicktarget': 'colorProductPrice'})
                    if sale_price_span:
                        product_info['sale_price'] = sale_price_span.text.strip()

                    if link in found:
                        preqtxt = found[link]
                    else:
                        psimpletxt, preqtxt = get_html(link)
                        found[link] = preqtxt

                    psoup = BeautifulSoup(preqtxt)

                    div_class = 'w-100 flex flex-wrap flex-row'
                    main_div = psoup.find('div', {'class': div_class})
                    if not main_div:
                        print(f"Main div not found for {link}")
                        continue
                    
                    image_urls = []
                    img_div = main_div.find('div', {'class': 'flex flex-wrap items-center flex-column-ns'})
                    if img_div:
                        # Find all img tags
                        img_tags = img_div.find_all('img')

                        # Extract the src attribute from each img tag

                        for img in img_tags:
                            if 'src' in img.attrs:
                                image_urls.append(img['src'])

                        # Print the list of image URLs
                        for url in image_urls:
                            print(url)

                    info_class = 'w-100 pa2'
                    info_div = psoup.find('div', {'class': info_class})
                    if info_div:
                        print(info_div)




                    