import pandas as pd
import os
from PIL import Image
import numpy as np
#load in our text data. If we ever have more data, can add dataset as an argument but for now is unnecessary
image_paths = {
    'csvape' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/csvape/csvape_images',
    'getpop' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/getpop/getpop_images',
    'mipod' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/mipod/images',
    'myvaporstore' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/myvaporstore/myvaporstore_images',
    'perfectvape' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/perfect_vape/perfectvape_images',
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
    'perfectvape' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/perfect_vape/perfectvape_scrape.csv',
    'vapedotcom' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapedotcom/vapedotcom_scrape.csv',
    'vapesourcing' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapesourcing/vapesourcing_scrape.csv',
    'vapewh' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapewh/vapewh_scrape.csv',
    'vapingdotcom' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapingdotcom/vapingdotcom_scrape.csv'
}
def get_text(path: str):
    data = {}
    path = os.path.expanduser("~") + path
    text_data = pd.read_csv(path)
    #generate our text by concatenating all text data we have available together.
    #for the vast majority of entries, this comes from only the "Flavor" column.
    for i in range(len(text_data)):
        curr = text_data.iloc[i,:]
        name = curr.Product
        desc = ""
        if not pd.isna(curr.Description):
            desc += curr.Description
        if not pd.isna(curr.description):
            desc += curr.description
        if not pd.isna(curr.Flavor):
            desc += curr.Flavor
        if desc == "":
            continue
        data[name] = desc
    return data

#match each product to its corresponding image.
def get_imgs(path: str, key: str):
    path = os.path.expanduser("~") + path
    files = os.listdir(path)
    try:
        name = next(x for x in files if key in x)
    except StopIteration:
        return 
    image = Image.open(path + '/' + name).convert('RGB')
    #image = image.resize((400,400),Image.LANCZOS)
    return image

topics = {
    'iced':  "The following text consists of the name and a description for the e-cigarette in the image: '{desc}'. Based on the text and/or the image, does this e-cigarette produce a cooling sensation when used? Look for key words like 'mint,' 'icy,' 'menthol,' or similar words in the text. Additionally, look for imagery like mint, mountains, or ice in the image. If these features are present in either the text, the image, or both answer with yes. If not, answer with no. If there is no e-cigarette in the image and the text doesn't describe an e-cigarette, answer with no.",
    
    'screen' : "The following text consists of the name and a description for the e-cigarette in the image: '{desc}'  Based on the text or the image, is there a screen on the device? Answer with either yes or no."
}
def make_prompt(text, topic):
    prompt = topics[topic].format(desc = text)
    user =   {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": prompt },
            ],
    }
    return user
'''
NO LONGER USED!!! Can re-work if zero-shot learning is not working, but I never found it to be necessary.
'''
#generate a conversation for our in-context few-shot learning. This process can be made more complex in the future,
#but for now a conversation will be built from a base prompt and a collection of description-answer pairs.

def make_conversation(descriptions, answers):
    base_prompt = "The following text consists of the name and a description for the e-cigarette in the image: '{desc}' \
               Based on the name of the vape, the image, and the description, this e-cigarette produce a cooling sensation w  when used? Look for key words like 'mint,' 'icy,' etc. Answer with yes or no."
    def make_prompt(text):
        prompt = base_prompt.format(desc = text)
        user =   {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": prompt },
                ],
        }
        return user
    def make_answer(ans):
        answer = {
            "role": "assistant",
            "content": [
                    {"type": "text", "text": ans},
                    ],
            }
        return answer
    conversation = []
    for i in range(len(descriptions)-1):
        conversation.append(make_prompt(descriptions[i]))
        conversation.append(make_answer(answers[i]))
    conversation.append(make_prompt(descriptions[-1]))
    return conversation