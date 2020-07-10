import torch
import torch.nn as nn


class NN(nn.Module):

    def __init__(self):
        super(NN, self).__init__()

        self.l1 = nn.Linear(4, 4)
        self.l2 = nn.Linear(4, 3)
        self.l3 = nn.Linear(3, 2)

        self.net = nn.Sequential(self.l1, nn.ReLU(), self.l2, nn.ReLU(), self.l3, nn.Sigmoid())

    def forward(self, out):
        out = torch.tensor(out, dtype=torch.float32)
        out = self.net(out)
        out = 2 * out - 1
        return out

    def init_weights(self):
        torch.nn.init.xavier_uniform_(self.l1.weight)
        torch.nn.init.xavier_uniform_(self.l2.weight)
        torch.nn.init.xavier_uniform_(self.l3.weight)
