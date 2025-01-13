from data import trim
from modules import VLMModule
import pandas as pd
import pickle
from PIL import Image
from transformers import AutoProcessor
import torch
def main():
    config = {"max_epochs": 100,
          # "val_check_interval": 0.2, # how many times we want to validate during an epoch
          "check_val_every_n_epoch": 1,
          "gradient_clip_val": 1.0,
          "accumulate_grad_batches": 4,
          "lr": 1e-5,
          "batch_size": 1,
          # "seed":2022,
          "num_nodes": 1,
          "warmup_steps": 50,
          "result_path": "./result",
          "verbose": True,
    }
    model = VLMModule.load_from_checkpoint("FLAVA_Final.ckpt", 
                map_location=lambda storage, loc: storage, config = config,
                model =model, weights = None)
    processor = AutoProcessor.from_pretrained("facebook/flava-full")
    with open("../ZeroShot/vapes.pkl", "rb") as file:
        data = pickle.load(file)
    image = []
    label = []
    for eg in data:
        key = eg[0]
        source = eg[1]
        img = Image.open(source).convert('RGB')
        img = trim(img)
        text_inputs = processor.tokenizer(text=key, truncation='longest_first', 
                                          padding = 'max_length', max_length=512, return_tensors = 'pt')
        image_inputs = processor.image_processor.preprocess(images = img, do_resize = True, 
                                                            crop_size = {'height': 224, 'width':  224}, 
                                                            do_center_crop = False)
        text_inputs['pixel_values'] = torch.tensor(image_inputs['pixel_values'][0])
        res = torch.argmax(model.model(text_inputs))
        image.append(source)
        if res == 0:
            label.append("No Screen")
        elif res == 1:
            label.append("Screen")
        else:
            label.append("Not a Vape")
    data = {"image" : image, "label" :  label}
    csv = pd.DataFrame(data)
    csv.to_csv("preds.csv", index = False)
if __name__ == "__main__":
    main()