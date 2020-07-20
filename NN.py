from typing import Dict

import torch
import torch.nn as nn
import numpy as np

class NN(nn.Module):

    def __init__(self):
        super(NN, self).__init__()

        self.l1 = nn.Linear(4, 4)
        self.l2 = nn.Linear(4, 4)
        self.l3 = nn.Linear(4, 4)

        self.net = nn.Sequential(self.l1, nn.ReLU(), self.l2, nn.ReLU(), self.l3, nn.Sigmoid())
        self.layer_nodes = len(self.net)

    def forward(self, out):
        out = torch.tensor(out, dtype=torch.float32)
        out = self.net(out)
        return out

    def init_weights(self):
        with torch.no_grad():
            torch.nn.init.xavier_uniform_(self.l1.weight)
            torch.nn.init.xavier_uniform_(self.l2.weight)
            torch.nn.init.xavier_uniform_(self.l3.weight)

    def transform_weights(self, params: Dict):
        W1 = params['W0']
        b1 = np.squeeze(params['b0'])
        W2 = params['W2']
        b2 = np.squeeze(params['b2'])
        W3 = params['W4']
        b3 = np.squeeze(params['b4'])
        self.set_weights(W1, b1, W2, b2, W3, b3)

    def set_weights(self, W1: np.ndarray, b1: np.ndarray,
                          W2: np.ndarray, b2: np.ndarray,
                          W3: np.ndarray, b3: np.ndarray):
        with torch.no_grad():
            self.l1.weight = torch.nn.Parameter(torch.from_numpy(W1).float())
            self.l1.bias = torch.nn.Parameter(torch.from_numpy(b1).float())
            self.l2.weight = torch.nn.Parameter(torch.from_numpy(W2).float())
            self.l2.bias = torch.nn.Parameter(torch.from_numpy(b2).float())
            self.l3.weight = torch.nn.Parameter(torch.from_numpy(W3).float())
            self.l3.bias = torch.nn.Parameter(torch.from_numpy(b3).float())

    def show(self):
        print("First Layer")
        print(self.l1)
        print(self.l1.weight)
        print(self.l1.bias)
        print()
        print("Second Layer")
        print(self.l2)
        print(self.l2.weight)
        print(self.l2.bias)
        print()
        print("Third Layer")
        print(self.l3)
        print(self.l3.weight)
        print(self.l3.bias)
        print()
        print()
        print(self.layer_nodes)
        for i in range(0, self.layer_nodes, 2):
            print(self.net[i])
