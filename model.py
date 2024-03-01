import argparse
import torch
import accelerate
import lightning
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import pytorch_lightning as pl
import torch.optim as optim
import pandas as pd
import json


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000, device=torch.device('cuda')):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, d_model).to(device, dtype=torch.float64)
        position = torch.arange(0, max_len, dtype=torch.float64).unsqueeze(1).to(device, dtype=torch.float64)
        div_term = torch.exp(torch.arange(0, d_model, 2).to(device, dtype=torch.float64) * (-torch.log(torch.tensor(10000.0)) / d_model)).to(device, dtype=torch.float64)
        pe[:, 0::2] = torch.sin(position * div_term).to(device, dtype=torch.float64)
        pe[:, 1::2] = torch.cos(position * div_term).to(device, dtype=torch.float64)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        return x + self.pe[:x.size(0), :]
    




def get_user_input() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Download stock data from Alpha Vantage.')
    parser.add_argument('-t', '--train', type=str, help='Symbol to train the model and model version', nargs=2)
    parser.add_argument('-e', '--eval', type=str, help='Company symbol to be evalueated and model version', nargs=2)
    
    return parser.parse_args()

def train_model_v0(symbol: str) -> None: ...

def train_model_v1(symbol: str) -> None: ...

def train_model_v2(symbol: str) -> None: ...

def eval_model_v0(symbol: str) -> None: ...

def eval_model_v1(symbol: str) -> None: ...

def eval_model_v2(symbol: str) -> None: ...

def train_model(symbol: str, model_version: str) -> None:
    symbol = symbol.upper()
    print(f'Training model for {symbol} with version {model_version}')
    match model_version:
        case 'v0': train_model_v0(symbol)
        case 'v1': train_model_v1(symbol)
        case 'v2': train_model_v2(symbol)
        case _: raise ValueError('Model version must be v0, v1 or v2')


def main():
    args = get_user_input()
    if args.train:
        if args.train[1] not in ['v0', 'v1', 'v2']:
            raise ValueError('Model version must be v0, v1 or v2')
        train_model(*args.train)


if __name__ == '__main__':
    main()