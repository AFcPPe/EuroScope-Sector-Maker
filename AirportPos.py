import os
import openpyxl

path = './nav/CIFP/'
dirs = os.listdir(path)

for each in dirs:
    with open(path+each)as f:
        data = f.read().split('\n')
        for line in data:
            if line[:3]=='RWY':
                print(line)