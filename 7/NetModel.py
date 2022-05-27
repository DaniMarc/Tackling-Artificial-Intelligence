import torch
import torch.nn.functional as F

class Net(torch.nn.Module):
    # the class for the network

    def __init__(self, n_feature, n_hidden, n_output):
        # we have two layers: a hidden one and an output one
        super(Net, self).__init__()
        # size of in/out
        self.hidden = torch.nn.Linear(n_feature, n_hidden)
        self.output = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):
        # Applies the rectified linear unit function element-wise (forward propagation of the signal).
        x = F.relu(self.hidden(x))
        x = self.output(x)
        return x