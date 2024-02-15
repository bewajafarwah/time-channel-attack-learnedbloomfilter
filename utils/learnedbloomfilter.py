import numpy as np
import torch
from utils.bloomfilter import BloomFilter

class LearnedModel:
    def __init__(self, model, input_size, thresh=0.5, device="cpu"):
        self.model = model
        self.device = device
        self.input_size = input_size
        self.thresh = torch.tensor(thresh, device=self.device)

        self.model = self.model.to(self.device)
    
    def _preprocess(self, x):   
        x = np.atleast_1d(x)      
        
        X = []
        for integer in x:
            _tmp = [int(bit) for bit in format(integer, f'0{self.input_size}b')]
            X.append(_tmp)
        X = torch.tensor(X, device=self.device, dtype=torch.float32) 
        return X

    def predict(self, x):
        x = self._preprocess(x)

        with torch.no_grad():
            logits = self.model(x)
            probs = torch.sigmoid(logits)
            preds = (probs > self.thresh).int()

        if self.device != "cpu":
            preds = preds.cpu()
        
        preds = preds.view((-1)).numpy()
        return preds
    
class LearnedBloomFilter:
    def __init__(self, lm: LearnedModel, fpr, positives) -> None:
        self.lm = lm
        self.fpr = fpr
        self.bfilter = self._build_bloom_filter(positives)

    def _build_bloom_filter(self, positives):
        x = np.atleast_1d(positives) 

        preds = self.lm.predict(positives)

        neg_indices = np.where(preds == 0)[0]
        
        self.n_bfilter = len(neg_indices)
        bfilter = BloomFilter(n=self.n_bfilter, fpr=self.fpr)

        for i in neg_indices:
            bfilter.add(positives[i])
        return bfilter

    def query(self, x):
        x = np.atleast_1d(x) 
        
        preds = self.lm.predict(x)

        neg_indices = np.where(preds == 0)[0]

        for i in neg_indices:
            if self.bfilter.query(x[i]):
                preds[i] = 1
        return preds