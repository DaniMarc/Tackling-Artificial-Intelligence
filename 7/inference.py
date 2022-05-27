import torch

import NetModel
import math
filePath = "myNet.pt"
nnetwork = NetModel.Net(2, 128, 1)

nnetwork.load_state_dict(torch.load(filePath))
nnetwork.eval()

while True:
    x = input("x = ")
    if x == "exit":
        exit()
    x = float(x)
    y = float(input("y = "))
    print(nnetwork(torch.tensor((x, y))).tolist())
    print(math.sin(x + y / math.pi))