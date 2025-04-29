import torch
import torch.nn as nn

#a classification head for our model. We are using linear probing on the features derived from the pre-trained FLAVA model
class MLP(nn.Module):
    #hidden dims is a list of the hidden dimensions we hope to use
    def __init__(self, hidden_dims, in_dim, out_dim, dropout = 0.4):
        super(MLP, self).__init__()
        layers = nn.ModuleList()
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(in_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))
            layers.append(nn.SiLU())
            if dropout > 0:
                layers.append(nn.Dropout(dropout))
            in_dim = hidden_dim
        layers.append(nn.Linear(in_dim, out_dim))
        self.model = nn.Sequential(*layers)
    def forward(self, x):
        return self.model(x)
'''
class ViLTClassification(nn.Module):
    def __init__(self, backbone, head):
        super(ViLTClassification, self).__init__()
        self.backbone = backbone
        self.head = 
    def forward(self, x):'''
        
#we pass our inputs through Flava to generate tokens. Then, we take the CLS token (at index zero) and feed through the prediction head
class FlavaClassification(nn.Module):
    def __init__(self, backbone, head):
        super(FlavaClassification, self).__init__()
        self.backbone = backbone
        #freeze model weights, allowing only the head to be trained
        '''
        Commenting out as PEFT automatically freezes existing model weights
        for param in self.backbone.parameters():
            param.requires_grad = False'''
        self.head = head
    
    def forward(self, x):
        #dict_keys(['input_ids', 'token_type_ids', 'attention_mask', 'pixel_values'])
        outputs = self.backbone(**x)
        tokens = outputs.multimodal_embeddings[:, 0, :]
        return self.head(tokens)
        