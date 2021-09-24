#!/usr/bin/env python
# coding: utf-8

import pickle
import os
import glob
import numpy as np

# basePath = 'data/ramseyExtracted'
basePath = 'data/walkerLongExtracted'
machines = [
    # 'ibmq_rome',
    'ibmq_bogota',
]
outPath = 'data'
# outPrefix = 'ramsey'
outPrefix = 'walkerLong'

# k = 200
k = 1000

windowSize = 10 #use windowSize elements to predict the windowSize+1

for machine in machines:
    print("========= Dataset with {} and k={}".format(machine,k))
    outDataset = '{}-dataset-{}-{}-{}.npz'.format(outPrefix, machine, k, windowSize)
    outSplit = '{}-split-{}-{}-{}.npz'.format(outPrefix, machine, k, windowSize)

    os.makedirs(outPath, exist_ok=True)
    np.random.seed(42)

    fileProb = os.path.join(basePath, 'probabilities-{}-{}.npy'.format(k,machine))
    print("Load probabilities in {}".format(fileProb))
    probabilities = np.load(fileProb)
    
    x = []
    y = []
    for i in range(probabilities.shape[0]-windowSize):
        currX = []
        for j in range(windowSize):
            currX.append(probabilities[i+j])
        x.append(currX)
        y.append(probabilities[i+windowSize])

    x = np.array(x, dtype='float32')
    y = np.array(y, dtype='float32')

    np.savez_compressed(os.path.join(outPath, outDataset), x=x, y=y)
    print("Saved dataset in {}".format(os.path.join(outPath, outDataset)))

    dataLen = len(y)
    testLen = int(dataLen / 100. * 20.)

    index = np.array(range(dataLen), dtype='int32')

    test = index[-testLen:]
    valid = index[-2 * testLen: -testLen]
    train = index[: -2 * testLen]

    np.savez_compressed(os.path.join(outPath, outSplit), train=train, valid=valid, test=test)
    print("Saved Split in {}".format(os.path.join(outPath, outSplit)))
