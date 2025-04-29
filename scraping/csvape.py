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


BASE = 'https://csvape.com' # https://csvape.com/collections/7-daze-salt-nicotine

links = [
    '/collections/disposable-vapes',
    '/collections/7-daze-eliquid',
    '/collections/aqua-nicotine-salts-eliquids-1',
    '/collections/coastal-clouds-salts',
    '/collections/cuttwood-ejuice',
    '/collections/dessert-flavors-e-liquid',
    '/collections/ejuice',
    '/collections/four-seasons-salts',
    '/collections/fruity-flavors-e-liquid',
    '/collections/glas-vapor-salt-nic',
    '/collections/jam-monster-eliquids',
    '/collections/jam-monster-salt-nic',
    '/collections/kilo-ejuice',
    '/collections/menthol-flavors-e-liquid',
    '/collections/naked-100',
    '/collections/pacha-mama',
    '/collections/pacha-mama-ejuice-brands',
    '/collections/reds-ejuice',
    '/collections/salt-nicotine-brands',
    '/collections/saltnic-labs',
    '/collections/shijin-vapor-salt-nic',
    '/collections/the-mamasan',
    '/collections/tobacco-flavors-e-liquid',
    '/collections/vgod-ejuice',
    '/collections/vgod-saltnic',
    '/collections/pod-systems',
    '/collections/tanks',
    '/collections/vape-accessories',
    '/collections/vape-starter-kits',
    '/collections/nicotine-pouches',
    '/collections/ecigara',
    '/collections/flavor-profile',
    '/collections/newarrivals',
    '/collections/vgod',
    '/collections/all',
]

print('TOTAL LINKS', len(links))
found = dict()


def get_html(url, clicked=False, closed=False, elements=True):

    driver = None
    try:
        options = Options()
        options.add_argument('--headless')  # Enable headless mode properly

        # Start the WebDriver in headless mode
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        last_n = 0
        hrefs = set()
        button_id = 'ac-ag-yes-button'

        html = driver.page_source
        time.sleep(1)
        same_count = 0
        if not clicked:
            wait = WebDriverWait(driver, 3)  # 10 seconds timeout
            button = wait.until(EC.element_to_be_clickable((By.ID, button_id)))  # Use ID, XPATH, or other locator

            # Click the button
            button.click()
            clicked = True
        if not closed:
            wait = WebDriverWait(driver, 3)  # 10 seconds timeout
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'close')))  # Use ID, XPATH, or other locator

            # Click the button
            button.click()
            closed = True
    

        # Set a delay for dynamic content loading
        SCROLL_PAUSE_TIME = 1  # Shorter pause for smoother scroll

        # Scroll incrementally by a small step (e.g., 500 pixels)
        scroll_increment = 750

        # Get the initial scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        first_height = last_height
        # print(last_height)

        while True:
            # Scroll down by the increment
            driver.execute_script(f"window.scrollBy(0, {scroll_increment});")

            # Wait for the page to load new content
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate the new scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")

            # Check if new elements have appeared on the screen
            # You can check specific elements like this:
            # elements = driver.find_elements(By.CLASS_NAME, "your-element-class")

            # If the scroll height has not changed, break the loop
            #print(same_count, new_height, last_height)
            if new_height == last_height :
                same_count += 1
                if same_count >= 3:
                    break
            else:
                same_count = 0

            # Update the last height
            last_height = new_height
        html = driver.page_source

    except Exception as ex:
        print(ex)
        html = ''
    finally:
        if driver:
            driver.close()
    time.sleep(3)


    return html

def extract_options(soup, header_name):
    options = []
    header = soup.find('span', text=header_name)
    if header:
        # Find the next div with the class 'block-swatch-list' containing the options
        option_div = header.find_next('div', class_='block-swatch-list')
        if option_div:
            inputs = option_div.find_all('input', class_='block-swatch__radio')
            for option in inputs:
                options.append(option['value'])
    return options

if __name__ == "__main__":
    from collections import Counter

    product_list = list()
    all_headers = list()
    header_counter = Counter(all_headers)
    header_samples = dict()
    
    has_header = False
    
    with open('scraping/data-latest/csvape_scrape.csv', mode='w') as file:

        for l in links:
            page = 1
            site_section = l.replace('/collections/', '')

            url = f'{BASE}{l}'

            if url in found:
                reqtxt = found[url]
            else:
                reqtxt = get_html(url)
                found[url] = reqtxt
            #reqtxt = get_html(url)
            soup = BeautifulSoup(reqtxt)
            products = soup.find_all('div', {'class': 'product-item'})
            print(url, len(products))

            for p in products:
                if not isinstance(p, element.Tag):
                    continue
                title = p.find("a", class_="product-item__title").text.strip()
                link = p.find("a", class_="product-item__title")['href']
                spe = p.find("span", class_="price--highlight")
                rpe = p.find("span", class_="price")
                sale_price = None
                reg_price = None


                if rpe:
                    rpe_txt = rpe.text.strip()
                else:
                    rpe_txt = None

                # if spe:
                #     sale_price = spe.text.strip().replace('Sale price', '')
                # else:
                #     sale_price = None
                if rpe_txt and 'Sale price' in rpe_txt:
                    sale_price = rpe_txt.replace('Sale price', '').strip()
                else:
                    print('price check')

                print(link)

                # if rpe:

                #     reg_price = rpe.text.strip().replace('Regular price', '')
                # else:
                #     reg_price = None


                tag = link.split('/')[-1]

                if product_exists(CS_VAPE, tag):
                    print('EXISTS', tag)
                    continue
                full_link = f'{BASE}{link}'

                img_urls = []

                if full_link in found:
                    reqtxt = found[full_link]
                else:
                    # print(full_link)
                    reqtxt = get_html(full_link, elements=False)
                    found[full_link] = reqtxt
                psoup = BeautifulSoup(reqtxt)
                txt = psoup.get_text()

                img_tag = psoup.find('img', class_='product-gallery__image')
                img_alt = None
                if img_tag and 'alt' in img_tag.attrs:
                    img_alt = img_tag['alt']

                if img_tag and 'data-srcset' in img_tag.attrs:
                    spl =  img_tag['data-srcset'].split(',')
                    for s in spl:
                        if s.strip().startswith('http'):
                            img_urls.append({'url': s.strip(), 'alt': img_alt})
                        elif s.strip().startswith('//'):
                            img_urls.append({'url': 'http:' + s.strip(), 'alt': img_alt})

                elif img_tag and 'data-zoom' in img_tag.attrs:
                    # Extract the URL from the data-zoom attribute
                    spl =  img_tag['data-zoom'].split(',')
                    for s in spl:
                        if s.strip().startswith('http'):
                            img_urls.append({'url': s.strip(), 'alt': img_alt})
                        elif s.strip().startswith('//'):
                            img_urls.append({'url':'http:' + s.strip(), 'alt': img_alt})


                else:
                    print('NO IMAGE URL', full_link)

                container = psoup.find('div', {'class': 'container container--flush'})
                if container:
                    items_to_remove = container.find('path')
                    if items_to_remove:
                        items_to_remove.decompose()
                    remove = container.find('script')
                    if remove:
                        remove.decompose()

                    remove = container.find('nav')
                    if remove:
                        remove.decompose()

                    remove = container.find('noscript')
                    if remove:
                        remove.decompose()
                    items_to_remove = container.find('div', {'class': 'product-block-list__item--reviews'})
                    if items_to_remove:
                        items_to_remove.decompose()

                    remove = container.find('li', {'class': 'social-media__item social-media__item--pinterest'})
                    if remove:
                        remove.decompose()
                    remove = container.find('li', {'class': 'social-media__item social-media__item--twitter'})
                    if remove:
                        remove.decompose()

                    remove = container.find('li', {'class': 'social-media__item social-media__item--facebook'})
                    if remove:
                        remove.decompose()
                    items_remove = container.find('div', {'class': 'product-form__payment-container'})
                    if items_remove:
                        items_remove.decompose()

                    remove = container.find('div', {'class': "product-block-list__item product-block-list__item--shipping"})
                    if remove:
                        remove.decompose()

                    title = container.find('h1', class_='product-meta__title').text.strip()

        #             # Extract price
        #             price = container.find('span', class_='price price--highlight').text.strip()
        #             compare_price = container.find('span', class_='price price--compare').text.strip()

                    stock_element = container.find('span', class_='product-form__inventory')

                    # Check the stock status text
                    if stock_element:
                        stock_status = stock_element.text.strip()
                    else:
                        stock_status = ""

                    section_map = dict()
                    description_text = ''
                    # Extract product description
                    description_div = container.find('div', class_='product-block-list__item--description')
                    
                    if description_div:
                        # Find the 'rte text--pull' div within the description div
                        rte_div = description_div.find('div', class_='rte text--pull')
                        
                        if rte_div:
                            # Extract the text from the rte_div
                            description_text = rte_div.get_text(strip=True)
                    section_map['description'] = description_text


                    flavors = []
                    colors = []
                    nicotine_strengths = []
                    bottle_sizes = []

                    product_lists = container.find_all('div', class_='product-form__option')
                    if product_lists:
                        for product_list in product_lists:
                            product_lists_text = product_list.get_text(strip=True)
                            blocks = product_list.find_all('div', class_='block-swatch')
                            options = product_list.parent.find_all('option')

                            if product_lists_text.lower().startswith('flavor'):
                                # Loop through each block and extract flavor name and disabled status
                                for block in blocks:
                                    name = block.find('span', class_='block-swatch__item-text').text
                                    is_disabled = 'block-swatch--disabled' in block.get('class', [])
                                    flavors.append(name)
                            elif product_lists_text.lower().startswith('color'):
                                if options:
                                    for o in options:
                                        val = o['value']
                                        try:
                                            float(val)
                                        except Exception as ex:
                                            colors.append(val)
                            elif product_lists_text.lower().startswith('nicotine strength'):
                                # Loop through each block and extract flavor name and disabled status
                                for block in blocks:
                                    name = block.find('span', class_='block-swatch__item-text').text
                                    is_disabled = 'block-swatch--disabled' in block.get('class', [])
                                    value, unit = extract_value_and_unit(name)
                                    if len(value) > 0:
                                        value = value[0]
                                    else:
                                        value = None
                                    if len(unit) > 0:   
                                        unit = unit[0]
                                    else:
                                        unit = None
                                    if value and unit:
                                        val = {
                                            'value': value,
                                            'unit': unit
                                        }
                                        nicotine_strengths.append(val)
                            elif product_lists_text.lower().startswith('salt nicotine'):
                                # Loop through each block and extract flavor name and disabled status
                                for block in blocks:
                                    name = block.find('span', class_='block-swatch__item-text').text
                                    is_disabled = 'block-swatch--disabled' in block.get('class', [])
                                    val_units = extract_salt_nic_val_and_unit(name)
                                    for v in val_units:
                                        val = {
                                            'value': v[0],
                                            'unit': v[1]
                                        }
                                        nicotine_strengths.append(val)
                            elif product_lists_text.lower().startswith('variant') or product_lists_text.lower().startswith('resistance') or product_lists_text.lower().startswith('capacity')  or product_lists_text.lower().startswith('denominations') or product_lists_text.lower().startswith('style') or product_lists_text.lower().startswith('bottle size'):
                                continue
                            else:
                                # 'Salt Nicotine:50mg (5%)30mg (3%)50mg (5%)'
                                print(product_lists_text)


                n = 0
                images = list()
                for i in img_urls:
                    n += 1
                    img = download_image(i['url'], tag, save_dir='data_from_sites_v2/csvape_images', alt=i['alt'])
                    # these seem to be the same
                    images.append(img)
                    break



                # Extracting product information
                product_data = {
                    'tag': tag,
                    "title": title,
                    "link": full_link,
                    "sale_price": sale_price,
                    "regular_price": reg_price,
                    "image_urls": images,
                    'flavor_list': flavors,
                    'color_list': colors,
                    'nicotine_strengths': nicotine_strengths,
                    'bottle_sizes': bottle_sizes,
                    "stock_status": stock_status,
                    'site_category': site_section,
                    'images': images,
                    'html': reqtxt,
                    'plain_text': txt,
                }
                desc_fields = ''
                for s, v in section_map.items():
                    if 'description' not in s:
                        s = s + '_description'
                    product_data[s] = v.replace('\xa0', ' ').strip()
                    if product_data[s] != '':
                        desc_fields += f'\n{product_data[s]}'

                feats = list()
                #print(desc_fields)
                feat = find_features(desc_fields)
                any_found, puffs_res, nico_res, ml_res, flav_text, dev_text = feat
                product_data['puffs'] = puffs_res
                product_data['nicotine_strength'] = nico_res
                product_data['eliquid_contents'] = ml_res
                if any_found:
                    #print(feat)
                    feats.append(feat)
                disposable,recharge,battery,mesh,usb,adjustable,found_flavs = features_to_cats(feats)
                product_data['disposable_bool'] = disposable
                product_data['rechargeable_bool'] = recharge
                product_data['battery_bool'] = battery
                product_data['mesh_bool'] = mesh
                product_data['usb_bool'] = usb
                product_data['adjustable_bool'] = adjustable

                map_product_data(CS_VAPE, product_data)

                #print(product_data)

                #product_list.append(product_data)

                #print(product_data.keys())



                if not has_header:
                    # Create a DictWriter object
                    writer = csv.DictWriter(file, fieldnames=product_data.keys())

                    # Write the header (column names)
                    writer.writeheader()
                    
                    has_header = True

                writer.writerow(product_data)