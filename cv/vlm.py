import pandas as pd
import numpy as np
import torch 
from transformers import AutoProcessor, LlavaNextForConditionalGeneration, BitsAndBytesConfig
from dataset import llava_vape_dataset
import pickle
import sys
import argparse


def run_hf(topic, batch_size = 1, max_gen = 5):
    #quantization: not necessary but can improve inference speed at the cost of some performance
    '''for i in range(torch.cuda.device_count()):
           print(torch.cuda.get_device_properties(i).name)
    torch.cuda.set_device(1)'''
    data = llava_vape_dataset(path = '../../data/zeroshot.pkl', topic = topic)
    quantization_config = BitsAndBytesConfig(
        load_in_8bit=True
    )
    model = LlavaNextForConditionalGeneration.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf", torch_dtype=torch.float16, device_map = 'auto')
    processor = AutoProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
    processor.tokenizer.padding_side = 'left'
    processor.tokenizer.max_length = 1700
    processor.tokenizer.truncation = True
    model.padding_side = 'right'
    model.eval()
    res = []
    for i in range(0, len(data)-batch_size, batch_size):
        print(i)
        eg, sources, keys = data.getbatch(i, min(len(data) -1,i+batch_size))
        eg = eg.to(model.device)
        #print(eg['input_ids'][0].shape)
        with torch.no_grad():
            #gen = model.generate(**eg, max_new_tokens=max_gen)
            try:
                gen = model.generate(**eg, max_new_tokens=max_gen)
            except RuntimeError:
                print("Index: " + str(i))
                for i in range(len(eg['input_ids'])):
                    print(eg['input_ids'][i].shape)
                for i in range(len(eg['image_sizes'])):
                    print(eg['image_sizes'][i])
        for i in range(len(gen)):
            res.append([sources[i], keys[i], processor.batch_decode(gen[i][-max_gen:],skip_special_tokens=True, clean_up_tokenization_spaces=False)])
    name = "zeroshot" + topic + ".pkl"
    with open(name, 'wb') as file:
        pickle.dump(res, file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--topic',help='Which variable to code for')
    parser.add_argument('-b', type = int, default = 32, help='Batch Size')
    args = parser.parse_args()
    run_hf(args.topic, args.b)
'''
texts = get_text()
    imgs = get_imgs(texts)
    #make sure cuda is available!!
    #print(torch.cuda.is_available())
    #create some prompts...
    print(torch.cuda.is_available())
    descriptions = [texts['Blackberry Cherry EBCREATE BC5000 Thermal Edition'], texts['Blue Razz Icy UT Bar'],
               texts['Peach Ice Fume Infinity'],texts['Milk Chocolate Flonq Max'], texts['USB-C Charger']
    images = [imgs['Blackberry Cherry EBCREATE BC5000 Thermal Edition'], imgs['Blue Razz Icy UT Bar'],
               imgs['Peach Ice Fume Infinity'],imgs['Milk Chocolate Flonq Max'], imgs['Peach Ice Lost Mary OS5000'], 
                 imgs['USB-C Charger']]
    #add one additional text. This is what the VLM will respond to.
    #descriptions.append(texts['Peach Ice Lost Mary OS5000']) For this we expect a 'yes' response
    descriptions.append(texts['Crazy Melon Geek Bar Pulse'])
    answers = ['No.', 'Yes.', 'Yes.', 'No.', 'Not a vape.']

    conversation = make_conversation(descriptions, answers)
    prompts = processor.apply_chat_template(conversation, add_generation_prompt=True)
    inputs = processor(text=prompts, images=images, padding=True, return_tensors="pt").to(model.device)
'''