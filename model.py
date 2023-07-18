import torch
import torch.nn as nn

class NeuralNetwork_Adjustable(nn.Module):
   
    def __init__(self, input_size, output_size, n_hidden_layers = 4, nnodes=32, init_weights = False):
        super(NeuralNetwork_Adjustable, self).__init__()
        
        self.hidden_layers = nn.ModuleList()
        self.layer1 = nn.Linear(input_size, nnodes)
        
        for i in range(n_hidden_layers):
            if i+2 == nnodes:
                break
            else:
                self.hidden_layers.append(nn.Linear(nnodes, nnodes))
        
        self.layerfin = nn.Linear(nnodes, output_size)
        
        if init_weights:
            
            a = (3**0.5/nnodes)
            torch.nn.init.uniform_(self.layer1.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layerfin.weight, a=-0.05, b=0.05)
            
            for layer in self.hidden_layers:
                torch.nn.init.uniform_(layer.weight, a=-a, b=a)
            
        
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax()
        
    def forward(self, x):
        
        x = self.layer1(x)
        x = self.relu(x)
        
        for layer  in self.hidden_layers:
            x = layer(x)
            x = self.relu(x)
            
        x = self.layerfin(x)
        x = self.sigmoid(x)
        return x

class NeuralNetwork(nn.Module):
    # Constructor to define the neural network architecture
    def __init__(self, input_size, output_size, nnode=32, init_weights = False):
        super(NeuralNetwork, self).__init__()
        self.layer1 = nn.Linear(input_size, nnode)
        #self.dropout1 = nn.Dropout(p=0.3)
        self.layer2 = nn.Linear(nnode, nnode)
       # self.dropout2 = nn.Dropout(p=0.3)
        self.layer3 = nn.Linear(nnode, nnode)
        self.layer4 = nn.Linear(nnode, nnode)
        self.layer5 = nn.Linear(nnode, nnode)
        self.layer6 = nn.Linear(nnode, nnode)
        self.layerfin = nn.Linear(nnode, output_size)
        
        if init_weights:
            a = (3**0.5/nnode)
            torch.nn.init.uniform_(self.layer6.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layer5.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layer4.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layer3.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layer2.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layer1.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layerfin.weight, a=-0.05, b=0.05)
        
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax()
        
    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
       # x = self.dropout1(x)
        x = self.layer2(x)
        x = self.relu(x)
        #x = self.dropout2(x)
        x = self.layer3(x)
        x = self.relu(x)
        x = self.layer4(x)
        x = self.relu(x)
        x = self.layer5(x)
        x = self.relu(x)
        x = self.layer6(x)
        x = self.relu(x)
        x = self.layerfin(x)
       # x = self.sigmoid(x)
        return x
    
class TrackNetwork(nn.Module):
    def __init__(self):
        super(TrackNetwork, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=32, kernel_size=28, stride=28)
        
        self.fc1 = nn.Linear(32*15,32)
        
        self.fc2 = nn.Linear(32, 32)
        
        self.fc3 = nn.Linear(32, 1)  
        self.relu = nn.ReLU() 
        self.sigmoid = nn.Sigmoid()
        self.dropout1 = nn.Dropout(p=0.5)
        
    def forward(self, x, key = None):
        x = self.conv1(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
       # x = self.dropout1(x)
        x = self.relu(x)
       # x = self.fc2(x)
       # x = self.relu(x)
        if key == 'train': 
            x = self.fc2(x)
            x = self.relu(x)
            x = self.fc3(x)
            x = self.sigmoid(x)
        return x

class NeuralNetworkHigh(nn.Module):
   
    def __init__(self, input_size, output_size, nnode=32, init_weights = False):
        super(NeuralNetworkHigh, self).__init__()
        self.layer1 = nn.Linear(input_size, nnode)
        self.dropout1 = nn.Dropout(p=0.3)
        self.layer2 = nn.Linear(nnode, nnode)
       # self.dropout2 = nn.Dropout(p=0.3)
        self.layer3 = nn.Linear(nnode, nnode)
        self.layer4 = nn.Linear(nnode, nnode)
        self.layerfin = nn.Linear(nnode, output_size)
        
        if init_weights:
            a = (3**0.5/nnode)
            torch.nn.init.uniform_(self.layer4.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layer3.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layer2.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layer1.weight, a=-a, b=a)
            torch.nn.init.uniform_(self.layerfin.weight, a=-0.05, b=0.05)
        
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax()
        
    def forward(self, x, key = None):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.dropout1(x)
        x = self.layer2(x)
        x = self.relu(x)
        #x = self.dropout2(x)
       # x = self.layer3(x)
       # x = self.relu(x)
       # x = self.layer4(x)
       # x = self.relu(x)
        if key == 'train':
            
            x = self.layerfin(x)
            x = self.sigmoid(x)
        return x
