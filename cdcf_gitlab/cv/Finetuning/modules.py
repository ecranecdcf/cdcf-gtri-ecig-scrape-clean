import lightning as L
#from data import collate_fn
import torch.nn as nn
import torch
from torchmetrics.classification import BinaryAccuracy
class VLMModule(L.LightningModule):
    def __init__(self, config, model, weights = None):
        super().__init__()
        self.config = config
        self.model = model
        if weights:
            self.loss = nn.CrossEntropyLoss(torch.Tensor(weights))
        else:
            self.loss = nn.CrossEntropyLoss()
        self.batch_size = config.get("batch_size")
        self.accuracy = BinaryAccuracy()

    def training_step(self, batch, batch_idx):
        x, y = batch
        
        pred = self.model(x)
        
        loss = self.loss(y,pred)

        self.log("train_loss", loss, sync_dist=True)
        acc = self.accuracy(torch.argmax(pred,dim=1), torch.argmax(y,dim=1))
        self.log("train_acc", acc, sync_dist=True)
        return loss

    def validation_step(self, batch, batch_idx):

        x, y = batch
        pred = self.model(x)
        
        loss = self.loss(y,pred)

        self.log("val_loss", loss, sync_dist=True)
        acc = self.accuracy(torch.argmax(pred,dim=1),  torch.argmax(y,dim=1))
        self.log("val_acc", acc, sync_dist=True)
        
        return loss

    def configure_optimizers(self):
        # you could also add a learning rate scheduler if you want
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.config.get("lr"))
        return optimizer
