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
import traceback


import json
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities




sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.db import *
from ecig_parsing import *


BASE = 'https://getpop.co' 
company = GETPOP

links = [
    '/collections/disposables/0mg-nicotine',
    '/collections/disposables/air-bar',
    '/collections/disposables/candy',
    '/collections/disposables/coffee',
    '/collections/disposables/fruity',
    '/collections/disposables/fume',
    '/collections/disposables/geek-bar',
    '/collections/disposables/hqd',
    '/collections/disposables/hyde',
    '/collections/disposables/ice',
    '/collections/disposables/kado-bar',
    '/collections/disposables/lost-mary',
    '/collections/disposables/mint',
    '/collections/disposables/raz',
    '/collections/disposables/rechargeable',
    '/collections/disposables/tobacco',
    '/collections/disposables',
    '/collections/e-liquids/Bakery',
    '/collections/e-liquids/Drinks%2FBeverages',
    '/collections/e-liquids/Fruity',
    '/collections/e-liquids/Mint',
    '/collections/e-liquids/Monster-Vape-Labs',
    '/collections/e-liquids/Pod-Juice',
    '/collections/e-liquids/Tobacco',
    '/collections/e-liquids/VGOD',
        '/collections/e-liquids',
    '/collections/devices',
    '/collections/pods',
    '/collections/pod-systems',
    '/collections/pod-systems/smok',
    '/collections/pod-systems/uwell',
    '/collections/pod-systems/vaporesso',
    '/collections/pod-systems/voopoo',
    '/collections/nicotine-pouches/chyl',
    '/collections/nicotine-pouches/fume',
    '/collections/nicotine-pouches/kado-bar',
    '/collections/nicotine-pouches/lucy',
    '/collections/nicotine-pouches/qit',
    '/collections/nicotine-pouches/zyn',
        '/collections/nicotine-pouches',
    '/collections/back-in-stock',
    '/collections/best-sellers',
    '/collections/flavor-of-the-month',
    '/collections/new-arrivals',
    '/collections/under-10',
    '/collections/all',
]

print('TOTAL LINKS', len(links))
found = dict()


def extract_flavor_ratings(soup, class_name='kl_reviews__summary__custom_question--range', split_on=' as an average of '):
    # Find all rating sections
    rating_sections = soup.find_all('div', class_=class_name)

    # Extract data for each rating
    ratings = {}
    for section in rating_sections:
        # Get the flavor/attribute name
        try:
            attribute = section.find('strong').text.strip()
            
            # Get the rating value from the aria-label attribute
            span_elem = section.find('span', attrs={'role': 'img'})
            if span_elem and 'aria-label' in span_elem.attrs:
                aria_label = span_elem['aria-label']
                # Extract the number using string manipulation
                # The format is typically "Reviewers rated X as an average of Y between..."
                parts = aria_label.split(split_on)
                if len(parts) > 1:
                    rating_value = parts[1].split(' ')[0]
                    ratings[attribute] = float(rating_value)
        except Exception as e:
            print(f"Error extracting flavor rating: {e}")
            traceback.print_exc()
            continue
    return ratings


def extract_reviews(soup):

    # Find all review items
    review_items = soup.find_all('div', class_='kl_reviews__review_item')
    if len(review_items) == 0:
        return []
    

    reviews = []
    
    for item in review_items:
        review = {}
        
        # Extract star rating
        stars_container = item.find('div', {'role': 'img'})
        if stars_container:
            aria_label = stars_container.get('aria-label', '')
            star_match = re.search(r'(\d+) star', aria_label)
            if star_match:
                review['rating'] = int(star_match.group(1))
            else:
                review['rating'] = None
        
        # Extract timestamp and convert to actual date
        timestamp_div = item.find('div', class_='kl_reviews__review__timestamp')
        if timestamp_div:
            relative_time = timestamp_div.text.strip()
            actual_date = convert_relative_time_to_date(relative_time)
            review['time'] = relative_time
            review['date'] = actual_date
        
        # Extract title
        title_div = item.find('div', class_='kl_reviews__review__title')
        if title_div and title_div.text.strip():
            review['title'] = title_div.text.strip()
        
        # Extract author name
        author_div = item.find('div', class_='kl_reviews__review__author')
        if author_div:
            name_div = author_div.find('div')
            if name_div:
                review['author'] = name_div.text.strip()
        
        # Check if verified buyer
        verified_span = item.find('span', class_='kl_reviews__review__verified')
        review['verified_buyer'] = bool(verified_span)
        
        # Extract review content
        content_p = item.find('p', class_='kl_reviews__review__content')
        if content_p:
            review['review_text'] = content_p.text.strip()
        
        # Extract variant info
        variant_p = item.find('p', class_='kl_reviews__review__variant')
        if variant_p:
            review['variant'] = variant_p.text.replace('Variant: ', '').strip()
        
        # Extract custom attributes (like Ice Level)
        attributes = {}
        custom_questions = item.find_all('div', class_='kl_reviews__custom_question_answer')
        
        for question in custom_questions:
            question_elem = question.find('strong')
            if question_elem:
                question_text = question_elem.text.strip()
                
                # Handle range-based answers
                if 'range' in question_elem.get('class', []):
                    spans = question.find_all('span')
                    if len(spans) >= 3:  # The range item itself plus the two label spans
                        aria_label = spans[0].get('aria-label', '')
                        value_match = re.search(r'rated .+ as a (\d+)', aria_label)
                        if value_match:
                            value = int(value_match.group(1))
                            attributes[question_text] = value
                else:
                    # Handle text-based answers
                    answer_elem = question.find('span', class_='kl_reviews__custom_question__answer')
                    if answer_elem:
                        attributes[question_text] = answer_elem.text.strip()
        
        if attributes:
            review['attributes'] = attributes
        
        # Extract images if any
        image_row = item.find('div', class_='kl_reviews__review__image_row')
        if image_row and image_row.find_all('img'):
            review['images'] = [img.get('src') for img in image_row.find_all('img')]

        flavor_ratings = extract_flavor_ratings(item, class_name='kl_reviews__custom_question_answer', split_on=' as a ')
        review['iced_level'] = flavor_ratings.get('Ice Level', None)
        review['sweet_level'] = flavor_ratings.get('Sweet Level', None)
        #review['flavor_ratings'] = flavor_ratings
        
        reviews.append(review)
    
    return reviews

def convert_relative_time_to_date(relative_time):
    """Convert relative time (e.g., '29 days ago') to an actual date string."""
    today = datetime.now()
    
    # Match patterns like "X days ago", "X weeks ago", etc.
    days_match = re.search(r'(\d+) days? ago', relative_time)
    weeks_match = re.search(r'(\d+) weeks? ago', relative_time)
    months_match = re.search(r'(\d+) months? ago', relative_time)
    years_match = re.search(r'(\d+) years? ago', relative_time)
    hours_match = re.search(r'(\d+) hours? ago', relative_time)
    minutes_match = re.search(r'(\d+) minutes? ago', relative_time)
    
    if days_match:
        days = int(days_match.group(1))
        date = today - timedelta(days=days)
    elif weeks_match:
        weeks = int(weeks_match.group(1))
        date = today - timedelta(weeks=weeks)
    elif months_match:
        months = int(months_match.group(1))
        # Approximate: a month as 30 days
        date = today - timedelta(days=months*30)
    elif years_match:
        years = int(years_match.group(1))
        # Approximate: a year as 365 days
        date = today - timedelta(days=years*365)
    elif hours_match:
        hours = int(hours_match.group(1))
        date = today - timedelta(hours=hours)
    elif minutes_match:
        minutes = int(minutes_match.group(1))
        date = today - timedelta(minutes=minutes)
    elif "just now" in relative_time.lower():
        date = today
    else:
        # If we can't parse it, return the original text
        return None
    
    return date.strftime('%Y-%m-%d')

def get_html(url, timeout=120):  # Added timeout parameter


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
        driver.set_page_load_timeout(timeout)
        driver.get(url)

        # Robust explicit wait: Wait for multiple elements or a specific element to be visible
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(5) #add a small sleep to ensure any javascript has finished.


    except Exception as ex:
        print(f"An error occurred: {ex}")
        traceback.print_exc()
        html = simple

    finally:
        if driver:
            html = driver.page_source
            driver.quit()
        else:
            html = simple

    return simple, html


def main():
    from collections import Counter

    product_list = list()
    all_headers = list()
    header_counter = Counter(all_headers)
    header_samples = dict()
    
    has_header = False
    
    with open(f'scraping/data-latest/{company}_scrape.csv', mode='w') as file:
        page = 1
        for l in links:
            
            page = 1
            site_section = l.replace('/collections/', '')

            while True:
                url = f'{BASE}{l}?page={page}'
                print(url)

                if url in found:
                    reqtxt = found[url]
                else:
                    simpletxt, reqtxt = get_html(url)
                    found[url] = reqtxt
                #reqtxt = get_html(url)
                soup = BeautifulSoup(reqtxt)
                products = soup.find_all('div', {'class': 'product-card'})
                print(url, len(products))
                
                if len(products) == 0:
                    break
                page += 1

                for p in products:
                    if not isinstance(p, element.Tag):
                        continue
                    title_ = p.find("h3", class_="product-card__title").text.strip()
                    brand_ = p.find("p", class_="product-card__vendor").text.strip()
                    brand_ = brand_.replace('Vendor:', '').strip()

                    brand = None
                    title = f'{brand_} {title_}' 
                    print('TITLE', title)

                    link = p.find("a", class_="reversed-link")['href']
                    rpe = p.find("span", class_="f-price-item")
                    sale_price = None
                    if rpe:
                        reg_price = rpe.text.strip()


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


                    print(link)

                    # if rpe:

                    #     reg_price = rpe.text.strip().replace('Regular price', '')
                    # else:
                    #     reg_price = None


                    tag = link.split('/')[-1]

                    if product_exists(company, tag):
                        print('EXISTS', tag)
                        continue
                    full_link = f'{BASE}{link}'

                    img_urls = []

                    if full_link in found:
                        reqtxt = found[full_link]
                    else:
                        # print(full_link)
                        simpletxt, reqtxt = get_html(full_link)
                        found[full_link] = reqtxt
                    print(full_link)
                    psoup = BeautifulSoup(reqtxt)
                    txt = psoup.get_text()

                    thumbnails = psoup.find('div', class_='product__media-gallery-thumbails')
                    gallery = psoup.find('div', class_='product__media-gallery-viewer-wrap')
                    img_tags = list()
                    if thumbnails:
                        img_tags.append(thumbnails.find_all('img'))
                    if gallery:
                        img_tags.append(gallery.find_all('img'))

                    for image_list in img_tags:
                        for img_tag in image_list:
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
                            elif img_tag and 'srcset' in img_tag.attrs:
                                spl =  img_tag['srcset'].split(',')
                                for s in spl:
                                    if s.strip().startswith('http'):
                                        img_urls.append({'url': s.strip(), 'alt': img_alt})
                                    elif s.strip().startswith('//'):
                                        img_urls.append({'url': 'http:' + s.strip(), 'alt': img_alt})
                            elif img_tag and 'src' in img_tag.attrs:
                                spl =  img_tag['src'].split(',')
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

                    container = psoup.find('div', {'class': 'product__blocks'})
                    flavors = []
                    colors = []
                    nicotine_strengths = []
                    bottle_sizes = []
                    product_contents = ''

                    if container:

                        # title = container.find('h1', class_='product__title').text.strip()

            #             # Extract price
            #             price = container.find('span', class_='price price--highlight').text.strip()
            #             compare_price = container.find('span', class_='price price--compare').text.strip()

                        stock_status = ""

                        section_map = dict()
                        description_text = ''
                        # Extract product description
                        highlights_div = container.find('div', class_='product__block--highlights-block')

                        if highlights_div:
                            summary = highlights_div.find('h2')
                            details = highlights_div.find_all('div', class_='items-center')

                            if summary:
                                description_text += summary.get_text(strip=True)
                            if details:
                                for d in details:
                                    description_text += d.get_text(strip=True)
                                    description_text += '\n'
                            description_text += '\n\n'
                            description_text = description_text.replace('HighlightsHighlights', 'Highlights ')
                        
                        product_blocks = container.find_all('div', class_='product__block--collapsible_tab')
                        if product_blocks:
                            for p in product_blocks:
                                summary = p.find('summary', class_='accordion-details__summary')
                                details = p.find('div', class_='accordion-details__content')

                                is_flavor = False
                                is_contents = False
                                if summary:
                                    sum_text = summary.get_text(strip=True)
                                    print(sum_text)
                                    description_text += sum_text
                                    description_text += '\n'
                                    if 'flavor' in sum_text.lower():
                                        is_flavor = True
                                    if "in the box" in sum_text.lower():
                                        is_contents = True
                                if details:
                                    details_text = details.get_text(strip=True)
                                    lis = details.find_all('li')
                                    if lis and len(lis) > 0:
                                        for l in lis:
                                            description_text += l.get_text(strip=True)
                                            description_text += '\n'

                                            if is_flavor:
                                                flavor = l.get_text(strip=True)
                                                if flavor and flavor not in flavors:
                                                    flavors.append(flavor)
                                            if is_contents:
                                                product_contents += l.get_text(strip=True)
                                                product_contents += '\n'

                                    else:
                                        description_text += details_text
                                    description_text += '\n'
                                description_text += '\n'

                        section_map['description'] = description_text



                    n = 0
                    images = list()
                    for i in img_urls:
                        n += 1
                        img = download_image(i['url'], tag, save_dir=f'data_from_sites_v2/{company}_images', alt=i['alt'])
                        # these seem to be the same
                        images.append(img)


                    reviews = extract_reviews(psoup)
                    review_attributes = extract_flavor_ratings(psoup)

                    # Extracting product information
                    product_data = {
                        'tag': tag,
                        "title": title,
                        'reviews': reviews,
                        'review_attributes': review_attributes,
                        'brand': brand,
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
                        'plain_text': txt.strip(),
                        'package_contents': product_contents,
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

                    product_data['battery'] = extract_battery(desc_fields)

                    map_product_data(company, product_data)

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


if __name__ == "__main__":
    do_update = False
    if do_update:
        results = get_products(GETPOP)

        for product_id, db_html, site_tag in results:
            print(product_id, site_tag)

            try:
                simple, html = get_html(f'https://getpop.co/products/{site_tag}')
                soup = BeautifulSoup(html)
                reviews = extract_reviews(soup)

                if len(reviews) > 0:
                    insert_reviews(reviews, product_id)

                rev_attributes = extract_flavor_ratings(soup)
                if len(rev_attributes.keys()) > 0:
                    insert_review_attributes(rev_attributes, product_id)
                time.sleep(1)
            except Exception as e:
                print(e)
                traceback.print_exc()
                continue
    else:
        main()