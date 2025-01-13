from transformers import AutoModel, AutoProcessor, AutoConfig
import torch
import os 
import lightning as L
from lightning.pytorch.callbacks import ModelCheckpoint
from lightning.pytorch.loggers import WandbLogger
from data import Flava_dataset, collate_fn
from torch.utils.data import DataLoader
from model import FlavaClassification, MLP
from modules import VLMModule
import argparse
import numpy as np
from peft import IA3Config, TaskType, get_peft_model
from sklearn.utils.class_weight import compute_class_weight

#remove .ipynb_checkpoints directory if necessary
def prepare(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir == ".ipynb_checkpoints":
                os.rmdir(os.path.join(root, dir))
                print(f"Removed: {os.path.join(root, dir)}")
                
#training and validation for the Flava model. It may be necessary to use distributed training since Flava is large, so 
#going to use vanilla pytorch here as opposed to huggingface's training interface
def main(args):
    #generate the indices for our training and validation sets
    path =  os.path.expanduser("~") +  "/CDCF_Webscrapping_Vape_Products_Project/testing/Finetuning/clean_data"
    prepare(path)
    num = len(os.listdir(path))
    nums = np.arange(num)
    train_indices = np.random.choice(nums, size = (int) (.8 * len(nums)), replace = False)
    val_indices = np.squeeze(nums[~np.isin(nums, train_indices)])
   
    #create our datasets and dataloaders
    train = Flava_dataset(path, train_indices)
    val = Flava_dataset(path, val_indices)
    train_loader = DataLoader(train, batch_size=args.batch, shuffle=True, drop_last = True, collate_fn = collate_fn)
    val_loader = DataLoader(val, batch_size=args.batch, shuffle=False, drop_last = True, collate_fn = collate_fn)
    labels = []
    for i in range(len(train)):
        try:
            labels.append(int(train[i][1]))
        except ValueError:
            labels.append(0)
    weights = compute_class_weight(class_weight = "balanced", classes = np.unique(labels), y = labels)
    #generate our model backbone
    configuration = AutoConfig.from_pretrained("facebook/flava-full")
    #configuration.text_config.max_position_embeddings= 750
    #configuration.image_config.image_size = 224
    backbone = AutoModel.from_pretrained("facebook/flava-full", config = configuration)
    hidden_size = backbone.config.hidden_size
    
    '''for m, _ in backbone.named_parameters():
        print(m)'''
    
    #initialize our LoRA finetuning paradigm. Can tune these params as well.
    peft_config = IA3Config(task_type=TaskType.SEQ_CLS, target_modules = ["dense"], feedforward_modules=["dense"])
    backbone = get_peft_model(backbone, peft_config)
    #classification head with 3 layers and 3 classes 
    cls_head = MLP([hidden_size, hidden_size, hidden_size], hidden_size, 2)
    model = FlavaClassification(backbone, cls_head)
    config = {"max_epochs": args.epochs,
          # "val_check_interval": 0.2, # how many times we want to validate during an epoch
          "check_val_every_n_epoch": 1,
          "gradient_clip_val": 1.0,
          "accumulate_grad_batches": 4,
          "lr": args.lr,
          "batch_size": args.batch,
          # "seed":2022,
          "num_nodes": 1,
          "warmup_steps": 50,
          "result_path": "./result",
          "verbose": True,
    }
    model_module = VLMModule(config, model, weights)
    wandb_logger = WandbLogger(project="Ecig-screen-final", name="IA3-dense")
    checkpoint_callback = ModelCheckpoint(dirpath="./model_checkpoints/IA3-dense", save_top_k=5, monitor="val_loss",filename="screen-{epoch}-{val_acc:.2f}")
    trainer = L.Trainer(
        accelerator="gpu",
        devices=[0],#torch.cuda.device_count(),
        #strategy="ddp",
        max_epochs=config.get("max_epochs"),
        accumulate_grad_batches=config.get("accumulate_grad_batches"),
        check_val_every_n_epoch=config.get("check_val_every_n_epoch"),
        gradient_clip_val=config.get("gradient_clip_val"),
        precision="16-mixed",
        #limit_val_batches=5,
        num_sanity_val_steps=0,
        logger=wandb_logger,
        callbacks=[checkpoint_callback],
        )
    trainer.fit(model_module, train_dataloaders = train_loader, val_dataloaders = val_loader)
        
if __name__ == "__main__":      
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='This script does something.')
    # Add arguments
    parser.add_argument('-epochs', "--epochs", type = int, default = 100, help='Number of fine-tuning epochs')
    parser.add_argument('-b', "--batch", type = int, default = 32, help = 'batch size')
    parser.add_argument('-lr', "--lr", type = float, default = 1e-5, help = "Learning Rate")
    # Parse the arguments
    args = parser.parse_args()
    main(args)
    