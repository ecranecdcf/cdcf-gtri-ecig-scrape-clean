# import spacy
# import en_core_web_sm
# nlp = en_core_web_sm.load()

import requests
import re
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd

from PIL import Image
from io import BytesIO
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

brands = ['7 Daze Reds Apple Salt',
 'Lucy Pouches',
 'Pod Juice x Hyde IQ 5000',
 'North 5000 ZERO',
 'Air Bar AB10000',
 'ORGNX 4000',
 'SVL BX12000',
 'HQD Cuvie Bar 7000',
 'Elf Bar BC5000',
 'Kado Bar x Pod King PK5000',
 'Hyde N-Bar Mini 2500',
 '7 Daze Ohmlet 7000',
 'Puff Plus',
 'Oxbar Magic Maze 2',
 'Pop HIT FLEX 3000',
 'Geek Bar Skyview 25K',
 'Air Bar ATRON 5000',
 'Fire ZERO 5000',
 'DigiFlavor x Geek Bar Lush 20K',
 'Space Mary SM8000',
 'Friobar DB7000',
 'VGOD Pod 1K',
 '7 Daze Egge 3000',
 'Pop HIT Solo 5500',
 'Lost Mary MO20000 PRO',
 'Block 6000',
 'UWELL',
 'Pod Juice Salt',
 'VGOD Pod 4K-R',
 'Pod Mesh FLO',
 'Air Bar AB5000',
 'HQD Cuvie Plus',
 'Pop Hit Salt',
 'Lost Mary OS5000 ZERO',
 'Pop HIT Bar 4000 ZERO',
 'Rama 16000',
 'Fume Pouches',
 'HandShake 15K Pod',
 'Hyppe Max Flow',
 'Puff Max 5000',
 'Bidi Stick 500',
 'Flum Pebble 6000',
 'Flum Float 3000',
 'Tyson 2.0 Round 2',
 'Monster Bars 3500',
 'Pop HIT Extra 3000 TFN',
 'Esco Bars Mesh 2500',
 'Hyde Edge RAVE Recharge',
 'Fume Ultra 2500',
 'Foodgod Zero',
 'VGOD Pod 1500',
 'Geek Bar Meloso Max 9000',
 'Kado Bar Vintage Edition 20K',
 'EB Create BC5000 Thermal Edition',
 'Mintopia 6000',
 'STIG',
 'Pod 5500',
 'VGOD SaltNic',
 'Esco Bars Mesh 6000',
 'Kado Bar BR5000',
 'Hyppe Max Air 5000',
 'Custard Monster Salt',
 'Geek Bar Pulse 15000',
 'STIG XL',
 'Kado Bar Pouches',
 'Squid 1.6K',
 'HQD Cuvie Air 4000',
 'Elf Bar ZERO BC5000',
 'Geek Bar B5000',
 'Fume Infinity 3500',
 'Jam Monster Salt',
 'Geek Bar Pulse X 25K',
 'The Milk Salt',
 'RAZ TN9000',
 'RabBeats RC10000 Touch',
 'Rare Mega 5000 Mesh',
 'Mr Fog Switch SW15000',
 'Air Bar Diamond 500',
 'Pod Pocket 7500',
 'Hyde X 3000',
 'Hyde N-Bar Recharge',
 'Tyson 2.0 Heavy Weight 7000',
 'Elux Cyberover 18000',
 'Geek Bar Meloso Mini 1500',
 'Air Bar Mini 2000',
 'Lost Vape Lightrise TB 18K',
 'Modus x Kado Bar KB10000',
 'Hyde x Pod Juice Salt',
 'Frozen Fruit Monster Salt',
 'Elf Bar BC5000 Ultra',
 'Pop HIT Bar 4000',
 'Lost Vape Orion Bar 10000',
 'Hyde Rebel Pro 5000',
 'Lost Mary BM5000',
 'Rare Bar 6000 Mesh',
 'Fume Extra',
 'RAZ CA6000',
 'SMOK Novo Bar AL6000',
 'Lost Mary OS5000',
 'Bliss Bar 5000',
 'Rare Palm 10000',
 'Lost Mary MT15000 Turbo',
 'Fruit Monster Salt',
 'Air Bar Diamond Box 20000',
 'TWIST 6000',
 'EB Design BC5000',
 'Air Bar Box 3000 by NKD100',
 'Air Bar Nex 6500',
 'Lost Vape Orion Bar 7500',
 'Puff Flow',
 'Air Bar Lux',
 'Flum GIO 3000',
 'Elf Bar x Pod King XC5000',
 'Air Bar Box 3000',
 'Oxbar Magic Maze Pro 10K',
 'Mintopia Turbo 9000',
 'Monster Bars Max 6000',
 'Strio x EB Create XC6500',
 'Elf Bar Airo Max 5000',
 'Pod 2500',
 'Kado Bar KB10000',
 'Hyde Edge Recharge',
 'EB Design TE6000',
 'Lost Mary OS5000 4%',
 'ORGNX Salt',
 'ZYN',
 'Lost Mary MO5000',
 'SMOK Spaceman Prism 20K',
 'Pop Pro',
 'Lucy Breakers',
 'North 5000 3%',
 'HQD Cuvie Plus 2.0',
 'PacksPod 5000',
 'North FT12000',
 'Hyde IQ Recharge',
 'QIT',
 'Hyde Retro RAVE Recharge',
 'Funky Republic Ti7000',
 'RAZ DC25000',
 'Fog X Box 6000',
 'Fume Eternity 20000',
 'Fume Unlimited 7000',
 'Fume Infinity Plus 4500',
 'Fifty Bar 6500']

brand_str = '''Juul
Hyde
Esco
Hyppe
Air Bar
Fume
Pod Juice
Lost Mary
Elf Bar
Kado Bar
Foodgood Zero
Monster Bars
Squid
Geek Bar
SMOK
Vuse
Blu
Njoy
MarkTen
Logic
Vapour2
Halo
Apollo
South Beach Smoke
Smok
Vaporesso
Innokin
Aspire
Eleaf
Joyetech
Geekvape
Uwell
Freemax
Vandy Vape
Wotofo
Lost Vape
Dovpo
Hellvape
Oumier
Augvape
Rincoe
OBS
Kangertech
Sigelei
iJoy
HQD
Foodgod
Pop
Flum
7 Daze
Teslacigs
EHPRO
Voopoo
Rincoe
Think Vape
iPV
Vapefly
Squid Industries
Purge Mods
The Vape Lounge
SvoëMesto
Revenant Vape
SnowWolf
Vaperz Cloud
Vicious Ant
ORGNX
Rare Mega
Rig Mod
Block
Rare Bar
Kennedy Vapor
Purge Ally
Deathwish Modz'''

brand_list = brand_str.split('\n')
brand_list.extend(brands)
brand_list = list(set(brands))

flavors = '''Chocolate
Vanilla
Strawberry
Blueberry
Raspberry
Cherry
Lemon
Lime
Orange
Grape
Watermelon
Apple
Pineapple
Mango
Peach
Apricot
Banana
Coconut
Caramel
Toffee
Butter
Peanut butter
Almond
Hazelnut
Pistachio
Mint
Peppermint
Spearmint
Cinnamon
Licorice
Anise
Root beer
Cola
Bubblegum
Cotton candy
Maple
Honey
Ginger
Espresso
Cappuccino
Irish cream
Rum
iced tea
Whiskey
Champagne
Red wine
White wine
Margarita
Pina colada
Mojito
Bloody Mary
Blue raspberry
Sour apple
Sour cherry
Sour lemon
Sour lime
Sour orange
Sour grape
Sour watermelon
Sour strawberry
Sour blueberry
Blackberry
Boysenberry
Cranberry
Elderberry
marshmallow
marshmallows
churro
churros
Kiwi
Passion fruit
Guava
Lychee
punch
Fig
Plum
Papaya
Black currant
Raspberry lemonade
Strawberry kiwi
Orange creamsicle
Key lime pie
Pomegranate
milk
Blueberry cheesecake
Peach cobbler
Apple pie
Pecan pie
melon
candy
cake
tropical
berry
cookie
lemonade
fruit punch
Mint chocolate chip
Chocolate fudge
Brownie batter
Cookies and cream
Rocky road
Snickerdoodle
ice cream
cola
menthol
Tiramisu
Chocolate truffle
Red velvet cake
Carrot cake
Lemon meringue pie
Grapefruit
Limeade
Pineapple upside down cake
Chocolate covered strawberry
Mint julep
Eggnog
berries
bubble gum
lemonade
Hot chocolate
Pumpkin spice
donut
gummy bear
snow cone
sno cone
fruit
fruity
tutti frutti
tutti-frutti
cinnamon
raspberry
blueberry
Margarita
Piña Colada
Daiquiri
coffee
soda
espresso
Mojito
Bloody Mary
Moscow Mule
Manhattan
Martini
Cosmopolitan
Long Island Iced Tea
Sex on the Beach
Mai Tai
Whiskey Sour
Tom Collins
Gin and Tonic
White Russian
Black Russian
butterscotch
Harvey Wallbanger
Tequila Sunrise
Paloma
Sangria
Mimosa
Bellini
Aperol Spritz
Negroni
Sazerac
Blue Hawaiian
Irish Coffee
Hot Toddy
Kamikaze
Lemon Drop Martini
Apple Martini
Espresso Martini
Chocolate Martini
Mojito Martini
Dirty Martini
espresso
lemon drop
Boulevardier
Salted caramel'''

words = '|'.join(list(set(flavors.split('\n'))))
flavor_regex = re.compile('({})'.format(words), flags=re.IGNORECASE)






# Function to download and save an image
def download_image(url, tag, save_dir='getpop_images'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    image_extension = url.split('.')[-1].split('?')[0].split(':')[0]  # Extract file extension from URL
    save_path = os.path.join(save_dir, f'{tag}.{image_extension}')
    if os.path.exists(save_path):
        #print(f"File already exists at {save_path}. Skipping download.")
        return
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for request errors
        img = Image.open(BytesIO(response.content))
        img.save(save_path)
        #print(f"Image saved: {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        
puff_regex = re.compile('([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-9][,][0-9][0-9][0-9]) puffs', flags=re.IGNORECASE)
nico_regex = re.compile('([1-9]\.[0-9][0-9]|[1-9][0-9]|[0-9]) ?%? ?nicotine', flags=re.IGNORECASE)
nico_regex2 = re.compile('([1-9]\.[0-9][0-9]|[1-9][0-9]|[0-9]) ?%? ?salt nicotine', flags=re.IGNORECASE)
device_regex = re.compile('(disposable|rechargeable|battery|mesh coil|USB|Adjustable Airflow)', flags=re.IGNORECASE)
ml_regex = re.compile('([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-9][,][0-9][0-9][0-9]) ?ml', flags=re.IGNORECASE)


def find_features(txt, section=None):
    p_text = ''
    n_text = ''
    ml_text = ''
    flav_text = []
    dev_text = []
    
    if section:
        txt2 = txt + ' ' + section
    else:
        txt2 = txt
    
    any_found = False
    puffs = puff_regex.search(txt)
    if puffs:
        p_text = (puffs.group(0))
        any_found = True

    
    nico = nico_regex.search(txt2)
    if nico:
        n_text = (nico.group(0))
        any_found = True
    else:
        nico2 = nico_regex2.search(txt2)
        if nico2:
            n_text = (nico2.group(0))
            any_found = True
            
    dev = device_regex.findall(txt)
    if dev:
        dev_text = dev
        any_found = True
        
    ml_ = ml_regex.search(txt)
    if ml_:
        ml_text = ml_.group(0)
        any_found = True
        
    flav_ = flavor_regex.findall(txt)
    if flav_:
        flav_text = flav_
        any_found = True
        
    return any_found, p_text, n_text, ml_text, flav_text, dev_text


def features_to_cats(feats):
    fl1 = ''
    fl2 = ''
    fl3 = ''
    fl5 = ''
    fl4 = ''
    disposable = ''
    recharge = ''
    battery = ''
    mesh = ''
    usb = ''
    adjustable = ''


    found_flavs = list()
    pe = ''
    pu = ''
    ml = ''
    for feat_ in feats:
        _, puffs_res, nico_res, ml_res, flav_text, dev_text = feat_
        if puffs_res and puffs_res != '':
            pu = puffs_res.lower().replace('puffs', '').replace(',', '').strip()
        if nico_res and nico_res != '':
            pe = nico_res.lower().replace('salt nicotine', '').replace('nicotine', '').strip()
        if ml_res and ml_res != '':
            ml = ml_res.lower().replace('ml', '').strip()
        if flav_text and len(flav_text) > 0:
            for ft in flav_text:
                found_flavs.append(ft.lower())

        if dev_text and  len(dev_text) > 0:
            #print(dev_text)
            for ft in dev_text:
                ft = ft.lower()
                #disposable','rechargeable','battery','mesh coil','USB','Adjustable Airflow',
                if 'disposable' == ft:
                    disposable = 'TRUE'
                if 'rechargeable' == ft:
                    recharge = 'TRUE'
                if 'battery' == ft:
                    battery = 'TRUE'
                if 'mesh coil' == ft:
                    mesh = 'TRUE'
                if 'usb' == ft:
                    usb = 'TRUE'
                if 'adjustable airflow' == ft:
                    adjustable = 'TRUE'
    found_flavs = sorted(list(set(found_flavs)))

    if len(found_flavs) == 5:
        fl1 = found_flavs[0]
        fl2 = found_flavs[1]
        fl3 = found_flavs[2]
        fl4 = found_flavs[3]
        fl5 = found_flavs[4]
    if len(found_flavs) == 4:
        fl1 = found_flavs[0]
        fl2 = found_flavs[1]
        fl3 = found_flavs[2]
        fl4 = found_flavs[3]
    if len(found_flavs) == 3:
        fl1 = found_flavs[0]
        fl2 = found_flavs[1]
        fl3 = found_flavs[2]
    if len(found_flavs) == 2:
        fl1 = found_flavs[0]
        fl2 = found_flavs[1]
    if len(found_flavs) == 1:
        fl1 = found_flavs[0]
        
    return disposable,recharge,battery,mesh,usb,adjustable,found_flavs

