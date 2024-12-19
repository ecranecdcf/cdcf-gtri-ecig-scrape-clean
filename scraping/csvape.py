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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ecig_parsing import *

BASE = 'https://csvape.com' # https://csvape.com/collections/7-daze-salt-nicotine

links = ['/collections/disposable-vapes', '/collections/pod-systems', '/collections/vape-starter-kits', '/collections/tanks', '/collections/vape-accessories', '/collections/vgod', '/collections/7-daze', '/collections/cuttwood-ejuice', '/collections/ecigara', '/collections/jam-monster-eliquids', '/collections/kilo-ejuice', '/collections/naked-100', '/collections/vgod-ejuice', '/collections/reds-ejuice', '/collections/vgod-saltnic', '/collections/saltnic-labs', '/collections/shijin-vapor-salt-nic', '/collections/glas-vapor-salt-nic', '/collections/coastal-clouds-salts', '/collections/pacha-mama-ejuice-brands', '/collections/jam-monster-salt-nic', '/collections/four-seasons-salts', '/collections/aqua-nicotine-salts-eliquids-1', '/collections/the-mamasan', '/collections/fruity-flavors-e-liquid', '/collections/dessert-flavors-e-liquid', '/collections/menthol-flavors-e-liquid', '/collections/tobacco-flavors-e-liquid', '/collections/vgod-ejuice', '/collections/reds-ejuice', '/collections/pacha-mama', '/collections/vgod-saltnic', '/collections/ejuice', '/collections/7-daze', '/collections/cuttwood-ejuice', '/collections/ecigara', '/collections/jam-monster-eliquids', '/collections/kilo-ejuice', '/collections/naked-100', '/collections/vgod-ejuice', '/collections/reds-ejuice', '/collections/salt-nicotine-brands', '/collections/vgod-saltnic', '/collections/saltnic-labs', '/collections/shijin-vapor-salt-nic', '/collections/glas-vapor-salt-nic', '/collections/coastal-clouds-salts', '/collections/pacha-mama-ejuice-brands', '/collections/jam-monster-salt-nic', '/collections/four-seasons-salts', '/collections/aqua-nicotine-salts-eliquids-1', '/collections/the-mamasan', '/collections/flavor-profile', '/collections/fruity-flavors-e-liquid', '/collections/dessert-flavors-e-liquid', '/collections/menthol-flavors-e-liquid', '/collections/tobacco-flavors-e-liquid', '/collections/all', '/collections/ejuice', '/collections/ejuice', '/collections/7-daze', '/collections/cuttwood-ejuice', '/collections/ecigara', '/collections/jam-monster-eliquids', '/collections/kilo-ejuice', '/collections/naked-100', '/collections/vgod-ejuice', '/collections/reds-ejuice', '/collections/salt-nicotine-brands', '/collections/vgod-saltnic', '/collections/saltnic-labs', '/collections/shijin-vapor-salt-nic', '/collections/glas-vapor-salt-nic', '/collections/coastal-clouds-salts', '/collections/pacha-mama-ejuice-brands', '/collections/jam-monster-salt-nic', '/collections/four-seasons-salts', '/collections/aqua-nicotine-salts-eliquids-1', '/collections/the-mamasan', '/collections/flavor-profile', '/collections/fruity-flavors-e-liquid', '/collections/dessert-flavors-e-liquid', '/collections/menthol-flavors-e-liquid', '/collections/tobacco-flavors-e-liquid', '/collections/vgod-ejuice', '/collections/reds-ejuice', '/collections/pacha-mama', '/collections/vgod-saltnic', '/collections/disposable-vapes', '/collections/pod-systems', '/collections/vape-starter-kits', '/collections/tanks', '/collections/vape-accessories', '/collections/vgod', '/collections/ejuice-brands', '/collections/salt-nicotine-brands', '/collections/flavor-profile', '/collections/voopoo-pod-systems', '/collections/vapeccino', '/collections/lost-vape-accessories', '/collections/suorin', '/collections/uwell', '/collections/replacement-pods-pod-systems', '/collections/pod-devices', '/collections/pod-ejuices', '/collections/disposable-vapes', '/collections/hyppe', '/collections/smok-vape', '/collections/vaporesso-vape-starter-kits', '/collections/all-in-one-starter-kits', '/collections/geek-vape-vape-starter-kits', '/collections/aspire-tanks', '/collections/tanks-brands', '/collections/sub-ohm-tanks', '/collections/tank-replacement-coils', '/collections/horizontech', '/collections/vape-battery-chargers', '/collections/replacement-glass', '/collections/mod-batteries', '/collections/replacement-atomizer-coils-vape-accessories', '/collections/replacement-pods-vape-accessories', '/collections/premade-rebuildable-coils', '/collections/accessories-brands', '/collections/replacement-vaporizers', '/collections/ejuice-brands', '/collections/salt-nicotine-brands', '/collections/flavor-profile', '/collections/voopoo-pod-systems', '/collections/vapeccino', '/collections/lost-vape-accessories', '/collections/suorin', '/collections/uwell', '/collections/replacement-pods-pod-systems', '/collections/pod-devices', '/collections/pod-ejuices', '/collections/disposable-vapes', '/collections/hyppe', '/collections/smok-vape', '/collections/vaporesso-vape-starter-kits', '/collections/all-in-one-starter-kits', '/collections/geek-vape-vape-starter-kits', '/collections/aspire-tanks', '/collections/tanks-brands', '/collections/sub-ohm-tanks', '/collections/tank-replacement-coils', '/collections/horizontech', '/collections/vape-battery-chargers', '/collections/replacement-glass', '/collections/mod-batteries', '/collections/replacement-atomizer-coils-vape-accessories', '/collections/replacement-pods-vape-accessories', '/collections/premade-rebuildable-coils', '/collections/accessories-brands', '/collections/replacement-vaporizers']

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
            wait = WebDriverWait(driver, 10)  # 10 seconds timeout
            button = wait.until(EC.element_to_be_clickable((By.ID, button_id)))  # Use ID, XPATH, or other locator

            # Click the button
            button.click()
            clicked = True
        if not closed:
            wait = WebDriverWait(driver, 10)  # 10 seconds timeout
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

            # if rpe:
                
            #     reg_price = rpe.text.strip().replace('Regular price', '')
            # else:
            #     reg_price = None
            
            
            tag = link.split('/')[-1]
            full_link = f'{BASE}{link}'
            
            img_urls = []

            if full_link in found:
                reqtxt = found[full_link]
            else:
                # print(full_link)
                reqtxt = get_html(full_link, elements=False)
                found[full_link] = reqtxt
            psoup = BeautifulSoup(reqtxt)

            img_tag = psoup.find('img', class_='product-gallery__image')
            
            if img_tag and 'data-srcset' in img_tag.attrs:
                spl =  img_tag['data-srcset'].split(',')
                for s in spl:
                    if s.strip().startswith('http'):
                        img_urls.append(s.strip())
                    elif s.strip().startswith('//'):
                        img_urls.append('http:' + s.strip())

            elif img_tag and 'data-zoom' in img_tag.attrs:
                # Extract the URL from the data-zoom attribute
                spl =  img_tag['data-zoom'].split(',')
                for s in spl:
                    if s.strip().startswith('http'):
                        img_urls.append(s.strip())
                    elif s.strip().startswith('//'):
                        img_urls.append('http:' + s.strip())

                
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

                # Extract product description
                desc_section = container.find(lambda tag: tag.name in ['strong','h1', 'h2', 'h3', 'h4', 'h5'] and tag.text.startswith('Description'))
                section_map = parse_description_sections(desc_section, all_headers, header_samples, full_link)

                flavor_blocks = container.find_all('div', class_='block-swatch')

                flavors = []

                # Loop through each block and extract flavor name and disabled status
                for block in flavor_blocks:
                    flavor_name = block.find('span', class_='block-swatch__item-text').text
                    is_disabled = 'block-swatch--disabled' in block.get('class', [])
                    flavors.append(flavor_name)
                    
            nicotine_strengths = extract_options(psoup, "Nicotine Strength")
            bottle_sizes = extract_options(psoup, "Bottle Size")
            
            n = 0
            for i in img_urls:
                n += 1
                download_image(i, tag, save_dir='scraping/data-2024-12/csvape_images')
                # these seem to be the same
                break



            # Extracting product information
            product_data = {
                'tag': tag,
                "title": title,
                "link": full_link,
                "sale_price": sale_price,
                "regular_price": reg_price,
                "image_urls": ','.join(img_urls),
                'flavor_list': flavors,
                'nicotine_strengths': nicotine_strengths,
                'bottle_sizes': bottle_sizes,
                "stock_status": stock_status,
                'site_category': site_section
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

            if any_found:
                #print(feat)
                feats.append(feat)
            disposable,recharge,battery,mesh,usb,adjustable,found_flavs = features_to_cats(feats)
            product_data['disposable'] = disposable
            product_data['rechargeable'] = recharge
            product_data['battery'] = battery
            product_data['mesh'] = mesh
            product_data['usb'] = usb
            product_data['adjustable'] = adjustable

            #print(product_data)
            
            product_list.append(product_data)



    print(len(product_list))

    with open('scraping/data-2024-12/csvape_scrape.csv', mode='w') as file:
        # Create a DictWriter object
        writer = csv.DictWriter(file, fieldnames=product_list[0].keys())

        # Write the header (column names)
        writer.writeheader()

        # Write the rows (each dictionary in the data list)
        writer.writerows(product_list)