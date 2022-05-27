import torch

import NetModel
from utils import *
import matplotlib.pyplot as plt


def loadData():
    return torch.load("myDataset.dat")


lossFunction = torch.nn.MSELoss()

nnetwork = NetModel.Net(n_feature=2, n_hidden=128, n_output=1).double()
data = loadData()
print(nnetwork)

# Stochastic Gradient Descent
optimizer_batch = torch.optim.SGD(nnetwork.parameters(), lr=LEARNING_RATE)

loss_list = []
average_loss_list = []
batch_number = len(data) // BATCH_SIZE

data_points = torch.tensor([(x[0], x[1]) for x in data])
split_points = torch.split(data_points, BATCH_SIZE)

data_values = torch.unsqueeze(torch.tensor([x[2] for x in data]), dim=1)
split_values = torch.split(data_values, BATCH_SIZE)

for epoch in range(NUMBER_EPOCHS):
    for batch in range(batch_number):
        batch_points = split_points[batch].double()
        batch_values = split_values[batch].double()

        #compute the output for the current batch 
        prediction = nnetwork(batch_points)

        #compute the loss for the current batch
        loss = lossFunction(prediction, batch_values)
        loss_list.append(loss.item())
        average_loss_list.append(loss.item() / BATCH_SIZE)

        #set up the gradients for the weights to zero
        optimizer_batch.zero_grad()
        
        #automatically compute the variation for each weight
        loss.backward()
        #compute the new values for the weights
        optimizer_batch.step()

    if epoch % 100 == 69:
        y_predictions = nnetwork(data_points.double())
        loss = lossFunction(y_predictions, data_values.double())
        print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

plt.plot(loss_list)
plt.savefig("graph.png")

plt.plot(average_loss_list)
plt.savefig("average.png")

filePath = "myNet.pt"
torch.save(nnetwork.state_dict(), filePath)

