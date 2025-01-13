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
ImageFile.LOAD_TRUNCATED_IMAGES = True

class llava_vape_dataset():
    #text data is expected to be in a csv, images in a file
    def __init__(self, path: str, topic: str):
        with open(path, 'rb') as data:
            arr = pickle.load(data)
        #randomly select about 25% of the data to work with
        choices = np.random.randint(0, len(arr), size = int(.25*len(arr)))
        self.data = [arr[i] for i in choices]
        #store only the path to accomodate larger datasets down the line
        self.processor = AutoProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
        self.processor.tokenizer.padding_side = 'left'
        self.processor.tokenizer.max_length = 1700
        self.processor.tokenizer.truncation = True
        self.topic = topic
    def __len__(self):
        return (len(self.data))
    def getbatch(self, start, end):
        prompts = []
        imgs = []
        keys = []
        sources = []
        for idx in range(start, end):
            eg = self.data[idx]
            source = eg[1]
            key = eg[0]
            #we dont have an image.
            img = Image.open(source).convert('RGB')
            lower = eg[5]
            upper = eg[4]
            left = eg[2]
            right = eg[3]
            #print(f"{upper} {lower} {left} {right}")
            if right - left < 40:
                left = max(0, left - 20)
                rigth = min(right + 20, img.size[0])
            if lower-upper < 40:
                upper = max(0, upper-20)
                lower = min(lower+20, img.size[1])
            img = img.crop((left,upper,right,lower))
            if(img.size[0] > 672):
                img = img.resize((672,672),Image.LANCZOS)
            img = np.asarray(img)
            #this portion will be slow and will tank device utilization. We could perform this offline and then
            #load pre-augmented batches, but this might not be necessary for our usecase. Will have to see...
            imgs.append(img) #self.inner_shot_image + [img]
            prompt = make_prompt(key, self.topic)
            prompts.append(self.processor.apply_chat_template([prompt], add_generation_prompt=True))
            keys.append(key)
            sources.append(source)
        inputs = self.processor(text=prompts, images=imgs, padding=True, return_tensors="pt")
        return inputs, sources, keys
