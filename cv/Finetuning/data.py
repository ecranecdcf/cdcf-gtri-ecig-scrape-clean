#this script will perform the preprocessing of our training, test, and validation set offline. This ensures that we can maximize GPU utilization
#during the fine-tuning process, which is critical to maximizing resource utilization
import pandas as pd
import torch
from transformers import AutoProcessor
from PIL import Image, ImageFile, ImageChops
import os
import pickle
ImageFile.LOAD_TRUNCATED_IMAGES = True

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
#since we performed our preprocessing offline, this step should be much less painful
def collate_fn(batch):
    #we need to maintain the class functions for transformers.tokenization_utils_base.BatchEncoding. So, the first member of the batch will be our 
    #leader and we will stack all of the tensors together, assigning them all to this first instance of the class
    text_tokens = torch.zeros((len(batch), 512), dtype=torch.int64)
    type_tokens = torch.zeros((len(batch), 512), dtype=torch.int64)
    attn_mask = torch.zeros((len(batch), 512), dtype = torch.int64)
    pixels = torch.zeros((len(batch), 3, 224, 224), dtype=torch.float32)
    labels = torch.zeros((len(batch), 2))
    for i, eg in enumerate(batch):
        text_tokens[i] = eg[0]['input_ids']
        type_tokens[i] = eg[0]['token_type_ids']
        attn_mask[i] = eg[0]['attention_mask']
        pixels[i] = eg[0]['pixel_values']
        try:
            label = int(eg[1])
        except: 
            label = 0
        labels[i][label] = 1
    res = batch[0][0]
    res['input_ids'] = text_tokens
    res['token_type_ids'] = type_tokens
    res['attention_mask'] = attn_mask
    res['pixel_values'] = pixels
    return res, labels
    
class Flava_dataset(torch.utils.data.Dataset):
    def __init__(self, root, indices):
        self.root = root
        self.files = os.listdir(root) # take all files in the root directory
        self.indices = indices
   
    def __len__(self):
        return len(self.indices)
    def __getitem__(self, idx):
        with open(os.path.join(self.root, self.files[self.indices[idx]]), "rb") as file:
            sample, label = pickle.load(file)
        return sample, label  
   
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    
def preprocess_data(name: str):
    raw_data = pd.read_csv('zeroshot-screen.csv')
    processor = AutoProcessor.from_pretrained("facebook/flava-full")
    processor.tokenizer.padding = True
    processor.tokenizer.padding_side = 'right'
    processor.tokenizer.max_length = 1500
    processor.tokenizer.truncation = True
    processor.image_processor.do_resize = False
    for i in raw_data.index:
        path = "clean_data/"
        eg = raw_data.loc[i,:]
        label = eg.label
        text = eg['description']
        if not isinstance(text, str):
            text = ""
        lower = eg.lower
        upper = eg.upper
        #mixed them up in the last step
        left = eg.right
        right = eg.left
        site = eg.site
        img = Image.open(eg.path).convert('RGB')
        if right - left < 40:
            left = max(0, left - 20)
            rigth = min(right + 20, img.size[0])
        if lower-upper < 40:
            upper = max(0, upper-20)
            lower = min(lower+20, img.size[1])
            
        img = img.crop((left,upper,right,lower))
        text_inputs = processor.tokenizer(text=text, truncation='longest_first', padding = 'max_length', max_length=512, return_tensors = 'pt')
        image_inputs = processor.image_processor.preprocess(images = img, do_resize = True, crop_size = {'height': 224, 'width':  224}, do_center_crop = False)
        text_inputs['pixel_values'] = torch.tensor(image_inputs['pixel_values'][0])
        with open(path + site + '_' + str(i) + '.pkl', 'wb') as file:
            pickle.dump((text_inputs, label), file)
if __name__ == "__main__":      
    preprocess_data('zeroshot-screen.csv')
    