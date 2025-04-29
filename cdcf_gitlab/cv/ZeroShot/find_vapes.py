import os
from PIL import Image
from ultralytics import YOLO
import numpy as np
import torch
import pandas as pd
import pickle 
import argparse

image_paths = {
    'csvape' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/csvape/csvape_images',
    'getpop' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/getpop/getpop_images',
    'mipod' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/mipod/images',
    'myvaporstore' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/myvaporstore/myvaporstore_images',
    'perfect_vape' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/perfect_vape/perfectvape_images',
    'vapedotcom' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapedotcom/vapedotcom_images',
    'vapesourcing' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapesourcing/vapesourcing_images',
    'vapewh' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapewh/vapewh_images',
    'vapingdotcom' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapingdotcom/vapingdotcom_images'

}
text_paths = {
    'csvape' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/csvape/csvape_scrape.csv',
    'getpop' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/getpop/getpop_ecig.csv',
    'mipod' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/mipod/product_type_mipod.csv',
    'myvaporstore': 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/myvaporstore/myvaporstore_scrape.csv',
    'perfect_vape' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/perfect_vape/perfectvape_scrape.csv',
    'vapedotcom' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapedotcom/vapedotcom_scrape.csv',
    'vapesourcing' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapesourcing/vapesourcing_scrape.csv',
    'vapewh' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapewh/vapewh_scrape.csv',
    'vapingdotcom' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapingdotcom/vapingdotcom_scrape.csv'
}
def get_text(site, name):
    #remove file extension (.jpg, .png, etc.)
    name = name[:name.find(".")]
    text_data = pd.read_csv(site)
       
    if  'mipod' in site:
        result = text_data[text_data.Product == name].reset_index(drop=True)
        if len(result) == 0:
            return "Name: " + name
        result = result.iloc[0, :]
        text = "Name: " + name +  " Description: "
        if not pd.isna(result.Description):
            text += result.Description
    else:
        result = text_data[text_data.tag == name].reset_index(drop=True)
        if len(result) == 0:
            return "Name: " + name
        result = result.iloc[0, :]
        text = "Name: " + name +  " Description: "
        if not pd.isna(result.description):
            text += result.description
    return text
def main(path):
    model = YOLO(path)
    base_path = os.path.expanduser("~") + "/../../"
    lst = []
    for key in image_paths.keys():
        images = os.listdir(base_path  + image_paths[key])
        for path in images:
            try:
                results = model(base_path + image_paths[key] + "/" + path)
            except ValueError:
                print(path)
            res = results[0].boxes
            #no vapes detected
            if not torch.any(res.cls == 1):
                continue
            #pick the most likely vape to be representative for this image
            vape = torch.argmax(res.conf[res.cls == 1]).item()
            coords = res.xyxy.cpu().detach().numpy()[vape]
            width = int(coords[2]) - int(coords[0])
            x =int(coords[0])
            y = int(coords[1])
            height = int(coords[3]) - int(coords[1])
            desc = get_text(base_path + text_paths[key], path)
            lst.append((desc, base_path + image_paths[key] + "/" + path, x, x + width, y, y+height))
    with open("vapes.pkl", 'wb') as file:
        pickle.dump(lst, file)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--path',help='Path to Yolo model')
    args = parser.parse_args()
    main(args.path)
