import torch
from torch.utils.data import Dataset
from utils import get_text, get_imgs, make_conversation, make_prompt
from transformers import AutoProcessor
from torch.utils.data import DataLoader
import pickle
from PIL import Image, ImageFile
import numpy as np
'''
This dataset is built to facilitate few-shot in-context learning with the open-sourced VLM Llava-NeXt
Llava-NeXt is a powerful model that can generalize to a wide-variety of tasks with little supervision.
These characteristics make it a smart choice for detecting vape features like iced or lcd screens, which
may be described in advertisements by text, images, or both.
'''
inner_shot_names = ['Blackberry Cherry EBCREATE BC5000 Thermal Edition', 'Blue Razz Icy UT Bar','Peach Ice Fume Infinity',
                   'Milk Chocolate Flonq Max','USB-C Charger']
inner_shot_answers =  ['No.', 'Yes.', 'Yes.', 'No.', 'Not a vape.']
ImageFile.LOAD_TRUNCATED_IMAGES = True

class llava_vape_dataset():
    #text data is expected to be in a csv, images in a file
    def __init__(self, path: str, topic: str):
        with open(path, 'rb') as data:
            self.data = pickle.load(data)
        #store only the path to accomodate larger datasets down the line
        self.processor = AutoProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
        self.processor.tokenizer.padding_side = 'left'
        self.processor.tokenizer.max_length = 1700
        self.processor.tokenizer.truncation = True
        self.topic = topic
        #TODO: add a functionality to improve selection of inner shots (annotated examples)
        #need to do some manual selection, but once chosen maybe store them in a pickle file?
        #want model to get a representative sample but not have so many that inference is painfull slow
        #for mipod, this short list should do the trick
        self.inner_shot_text = []
        self.inner_shot_image = []
        #self.make_inner_shots() 
    def __len__(self):
        return (len(self.data))
    def getbatch(self, start, end):
        prompts = []
        imgs = []
        keys = []
        sources = []
        for idx in range(start, end):
            eg = self.data[idx]
            source = eg[0]
            key = eg[1]
            txt = eg[2]
            #we dont have an image.
            if eg[3] == "":
                img = np.zeros((256,256,3))
            else:
                img = Image.open(eg[3]).convert('RGB')
                if(img.size[0] > 600):
                    img = img.resize((600,600),Image.LANCZOS)
                    img = np.array(img)
            #this portion will be slow and will tank device utilization. We could perform this offline and then
            #load pre-augmented batches, but this might not be necessary for our usecase. Will have to see...
            imgs.append(img) #self.inner_shot_image + [img]
            string = key + ':' + txt
            prompt = make_prompt(string, self.topic)
            prompts.append(self.processor.apply_chat_template([prompt], add_generation_prompt=True))
            keys.append(key)
            sources.append(source)
        inputs = self.processor(text=prompts, images=imgs, padding=True, return_tensors="pt")
        return inputs, sources, keys
