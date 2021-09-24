#!/usr/bin/env python
# coding: utf-8

import pickle
import os
import sys
import glob
import numpy as np

# basePath = 'data/walkerExtracted'
# basePath = 'data/walkerSlow1000Extracted'
# basePath = 'data/walkerSlow1500Extracted'
basePath = 'data/walkerSlowExtracted'
# basePath = 'data/walkerSimpleExtracted'
# basePath = 'data/walkerSingleMeasuresExtracted'
machinesGroups = [
    # ['ibmq_athens', 'ibmq_santiago'],
    # ['ibmq_casablanca', 'ibmq_santiago'],
    # ['ibmq_casablanca', 'ibmq_casablanca-bis'],
    # ['ibmq_casablanca', 'ibmq_casablanca'],
    # ['ibmq_athens-splitA', 'ibmq_athens-splitB'],
    # ['ibmq_athens-split10A', 'ibmq_athens-split10B'],
    # ['ibmq_athens-split10A', 'ibmq_athens-split10C'],
    # ['ibmq_athens-split10A', 'ibmq_athens-split10D'],
    # ['ibmq_athens-split10A', 'ibmq_athens-split10E'],
    # ['ibmq_athens-split10A', 'ibmq_athens-split10F'],
    # ['ibmq_athens-split10A', 'ibmq_athens-split10G'],
    # ['ibmq_athens-split10A', 'ibmq_athens-split10H'],
    # ['ibmq_athens-split10A', 'ibmq_athens-split10I'],
    # ['ibmq_athens-split10A', 'ibmq_athens-split10J'],
    # ['ibmq_5_yorktown', 'ibmq_athens', 'ibmq_bogota', 'ibmq_casablanca', 'ibmq_santiago']
    # ['ibmq_5_yorktown', 'ibmq_casablanca']
    # ['ibmq_belem', 'ibmq_quito']

    # walker: ['ibmq_athens', 'ibmq_bogota', 'ibmq_casablanca', 'ibmq_lima, 'ibmq_quito, 'ibmq_santiago', 'ibmq_5_yorktown']
    # ['ibmq_athens', 'ibmq_bogota'],
    # ['ibmq_athens', 'ibmq_casablanca'],
    # ['ibmq_athens', 'ibmq_lima'],
    # ['ibmq_athens', 'ibmq_quito'],
    # ['ibmq_athens', 'ibmq_santiago'],
    # ['ibmq_athens', 'ibmq_5_yorktown'],
    # ['ibmq_bogota', 'ibmq_casablanca'],
    # ['ibmq_bogota', 'ibmq_lima'],
    # ['ibmq_bogota', 'ibmq_quito'],
    # ['ibmq_bogota', 'ibmq_santiago'],
    # ['ibmq_bogota', 'ibmq_5_yorktown'],
    # ['ibmq_casablanca', 'ibmq_lima'],
    # ['ibmq_casablanca', 'ibmq_quito'],
    # ['ibmq_casablanca', 'ibmq_santiago'],
    # ['ibmq_casablanca', 'ibmq_5_yorktown'],
    # ['ibmq_lima', 'ibmq_quito'],
    # ['ibmq_lima', 'ibmq_santiago'],
    # ['ibmq_lima', 'ibmq_5_yorktown'],
    # ['ibmq_quito', 'ibmq_santiago'],
    # ['ibmq_quito', 'ibmq_5_yorktown'],
    # ['ibmq_santiago', 'ibmq_5_yorktown'],

    # multiclass complete
    # ['ibmq_athens', 'ibmq_bogota', 'ibmq_casablanca', 'ibmq_lima', 'ibmq_quito', 'ibmq_santiago', 'ibmq_5_yorktown'],

    # walkerSlow: ['ibmq_belem', 'ibmq_bogota', 'ibmq_quito', 'ibmq_rome]
    # ['ibmq_belem', 'ibmq_quito']

    # walkerSlow single temporal
    ['ibmq_belem']
]
outPath = 'data'
# outPrefix = 'walker'
# outPrefix = 'walkerSlow1000'
# outPrefix = 'walkerSlow1500'
# outPrefix = 'walkerSlow'
outPrefix = 'walkerSlowTemporal'
# outPrefix = 'walkerSimple'
# outPrefix = 'walkerSingleMeasures'
shuffle = True
# shuffle = False
testValidPercent = 20.
# testValidPercent = 25.
customSplits = {
    'A': ((0,200), (400,600), (800,1000)),
    'B': ((0,200), (200,400), (600,800)),

    'C1a': ((0,200), (200,400), (400,600)),
    'C2a': ((0,200), (600,800), (800,1000)),
    'C3a': ((0,200), (1000,1200), (1200,1400)),
    'C4a': ((0,200), (1400,1600), (1600,1800)),
    'C5a': ((0,200), (1800,2000), (1800,2000)),

    'C1b': ((200,400), (0,200), (400,600)),
    'C2b': ((200,400), (600,800), (800,1000)),
    'C3b': ((200,400), (1000,1200), (1200,1400)),
    'C4b': ((200,400), (1400,1600), (1600,1800)),
    'C5b': ((200,400), (1800,2000), (1800,2000)),

    'C1c': ((400,600), (0,200), (200,400)),
    'C2c': ((400,600), (600,800), (800,1000)),
    'C3c': ((400,600), (1000,1200), (1200,1400)),
    'C4c': ((400,600), (1400,1600), (1600,1800)),
    'C5c': ((400,600), (1800,2000), (1800,2000)),

    'C1d': ((600, 800), (0, 200), (200, 400)),
    'C2d': ((600, 800), (400, 600), (800, 1000)),
    'C3d': ((600, 800), (1000, 1200), (1200, 1400)),
    'C4d': ((600, 800), (1400, 1600), (1600, 1800)),
    'C5d': ((600, 800), (1800, 2000), (1800, 2000)),

    'C1e': ((800, 1000), (0, 200), (200, 400)),
    'C2e': ((800, 1000), (400, 600), (600, 800)),
    'C3e': ((800, 1000), (1000, 1200), (1200, 1400)),
    'C4e': ((800, 1000), (1400, 1600), (1600, 1800)),
    'C5e': ((800, 1000), (1800, 2000), (1800, 2000)),

    'C1f': ((1000, 1200), (0, 200), (200, 400)),
    'C2f': ((1000, 1200), (400, 600), (600, 800)),
    'C3f': ((1000, 1200), (800, 1000), (1200, 1400)),
    'C4f': ((1000, 1200), (1400, 1600), (1600, 1800)),
    'C5f': ((1000, 1200), (1800, 2000), (1800, 2000)),

    'C1g': ((1200, 1400), (0, 200), (200, 400)),
    'C2g': ((1200, 1400), (400, 600), (600, 800)),
    'C3g': ((1200, 1400), (800, 1000), (1000, 1200)),
    'C4g': ((1200, 1400), (1400, 1600), (1600, 1800)),
    'C5g': ((1200, 1400), (1800, 2000), (1800, 2000)),

    'C1h': ((1400, 1600), (0, 200), (200, 400)),
    'C2h': ((1400, 1600), (400, 600), (600, 800)),
    'C3h': ((1400, 1600), (800, 1000), (1000, 1200)),
    'C4h': ((1400, 1600), (1200, 1400), (1600, 1800)),
    'C5h': ((1400, 1600), (1800, 2000), (1800, 2000)),

    'C1i': ((1600, 1800), (0, 200), (200, 400)),
    'C2i': ((1600, 1800), (400, 600), (600, 800)),
    'C3i': ((1600, 1800), (800, 1000), (1000, 1200)),
    'C4i': ((1600, 1800), (1200, 1400), (1400, 1600)),
    'C5i': ((1600, 1800), (1800, 2000), (1800, 2000)),

    'C1j': ((1800, 2000), (0, 200), (200, 400)),
    'C2j': ((1800, 2000), (400, 600), (600, 800)),
    'C3j': ((1800, 2000), (800, 1000), (1000, 1200)),
    'C4j': ((1800, 2000), (1200, 1400), (1400, 1600)),
    'C5j': ((1800, 2000), (1600, 1800), (1800, 2000)),
}
customSplit = None
# customSplit = 'C5'
# customSplit = sys.argv[1]

shuffleAfter = False
# shuffleAfter = True

temporalDataset = None
# temporalDataset = 200
# temporalDataset = 400

customTemporalSplits = {
    'A1': ((0, 200), (200, 400)),
    'A2': ((0, 200), (400, 600)),
    'A3': ((0, 200), (600, 800)),
    'A4': ((0, 200), (800, 1000)),
    'A5': ((0, 200), (1000, 1200)),
    'A6': ((0, 200), (1200, 1400)),
    'A7': ((0, 200), (1400, 1600)),
    'A8': ((0, 200), (1600, 1800)),
    'A9': ((0, 200), (1800, 2000)),

    'B1': ((0, 200), (200, 400)),
    'B2': ((0, 200), (210, 410)),
    'B3': ((0, 200), (220, 420)),
    'B4': ((0, 200), (230, 430)),
    'B5': ((0, 200), (240, 440)),
    'B6': ((0, 200), (250, 450)),
    'B7': ((0, 200), (260, 460)),
    'B8': ((0, 200), (270, 470)),
    'B9': ((0, 200), (280, 480)),
    'B10': ((0, 200), (290, 490)),
    'B11': ((0, 200), (300, 500)),
    'B12': ((0, 200), (310, 510)),
    'B13': ((0, 200), (320, 520)),
    'B14': ((0, 200), (330, 530)),
    'B15': ((0, 200), (340, 540)),
    'B16': ((0, 200), (340, 540)),
    'B17': ((0, 200), (350, 550)),
    'B18': ((0, 200), (360, 560)),
    'B19': ((0, 200), (370, 570)),
    'B20': ((0, 200), (380, 580)),
    'B21': ((0, 200), (390, 590)),
    'B22': ((0, 200), (400, 600)),
}
for i in range(100):
    customTemporalSplits["C{}".format(i+1)] = ((0, 200), (200+i, 400+i))

for j,w in enumerate([(0, 200), (200, 400), (600, 800), (800, 1000), (1000, 1200)]):
    for i in range(600):
        customTemporalSplits["D-{}-{}".format(j+1, i+1)] = (w, (w[0]+200+i, w[1]+200+i))

for j,w in enumerate([(0, 400), (400, 800), (800, 1200)]):
    for i in range(400):
        customTemporalSplits["E-{}-{}".format(j+1, i+1)] = (w, (w[0]+400+i, w[1]+400+i))

for j,w in enumerate([(0, 400), (400, 800), (800, 1200)]):
    for i in range(2000-(w[1]+400)):
        customTemporalSplits["F-{}-{}".format(j+1, i+1)] = (w, (w[0]+400+i, w[1]+400+i))


# customTemporalDataset = None
# customTemporalDataset = 'A1'
customTemporalDataset = sys.argv[1]


# k = 200
k = 1000

for machines in machinesGroups:
    print("========= Dataset with {} and k={}".format(machines,k))
    outDataset = '{}-dataset-{}-{}{}{}{}.npz'.format(
        outPrefix,
        "-".join(machines),
        k,
        "" if shuffle else "-noShuffle",
        "" if temporalDataset is None else "-temporal{}".format(temporalDataset),
        "" if customTemporalDataset is None else "-customTemporal{}".format(customTemporalDataset)
    )
    outSplit = '{}-split-{}-{}{}{}{}{}{}{}.npz'.format(
        outPrefix,
        "-".join(machines),
        k,
        "" if shuffle else "-noShuffle",
        "" if not shuffleAfter else "-shuffleAfter",
        "" if not customSplit is None or testValidPercent == 20. else "-{}".format(int(testValidPercent)),
        "" if customSplit is None else "-customSplit{}".format(customSplit),
        "" if temporalDataset is None else "-temporal{}".format(temporalDataset),
        "" if customTemporalDataset is None else "-customTemporal{}".format(customTemporalDataset)
    )

    os.makedirs(outPath, exist_ok=True)
    np.random.seed(42)

    probabilities = []
    order = []
    for m in machines:
        fileProb = os.path.join(basePath, 'probabilities-{}-{}.npy'.format(k,m))
        print("Load probabilities in {}".format(fileProb))
        if not temporalDataset is None:
            originalProbabilities = np.load(fileProb)
            if originalProbabilities.shape[0] % temporalDataset != 0:
                raise ValueError("TemporalDataset not compatible with shape")
            for startIndex in range(0, originalProbabilities.shape[0], temporalDataset):
                probabilities.append(originalProbabilities[startIndex:startIndex+temporalDataset])
                if shuffle:
                    order.append(np.random.permutation(probabilities[-1].shape[0]))
                else:
                    order.append(np.array(range(probabilities[-1].shape[0])))
        elif not customTemporalDataset is None:
            originalProbabilities = np.load(fileProb)
            for (startIndex,endIndex) in customTemporalSplits[customTemporalDataset]:
                probabilities.append(originalProbabilities[startIndex:endIndex])
                if shuffle:
                    order.append(np.random.permutation(probabilities[-1].shape[0]))
                else:
                    order.append(np.array(range(probabilities[-1].shape[0])))
        else:
            probabilities.append(np.load(fileProb))
            if shuffle:
                order.append(np.random.permutation(probabilities[-1].shape[0]))
            else:
                order.append(np.array(range(probabilities[-1].shape[0])))



    x = []
    y = []
    for i in range(min(map(len, order))): #take min size if different
        for p in range(len(probabilities)):
            x.append(probabilities[p][order[p][i]])
            y.append(p)
            # currY = np.zeros((len(probabilities)), dtype='float32') #one hot encoding
            # currY[p] = 1.
            # y.append(currY)

    x = np.array(x, dtype='float32')
    y = np.array(y, dtype='int64')

    np.savez_compressed(os.path.join(outPath, outDataset), x=x, y=y)
    print("Saved dataset in {}".format(os.path.join(outPath, outDataset)))

    dataLen = len(y)
    index = np.array(range(dataLen), dtype='int32')

    if customSplit is None:
        testLen = int(dataLen / 100. * testValidPercent)
        test = index[-testLen:]
        valid = index[-2 * testLen: -testLen]
        train = index[: -2 * testLen]
    else:
        cs = customSplits[customSplit]
        train = index[cs[0][0]:cs[0][1]]
        valid = index[cs[1][0]:cs[1][1]]
        test = index[cs[2][0]:cs[2][1]]

    if shuffleAfter:
        np.random.shuffle(test)
        np.random.shuffle(valid)
        np.random.shuffle(train)

    np.savez_compressed(os.path.join(outPath, outSplit), train=train, valid=valid, test=test)
    print("Saved Split in {}".format(os.path.join(outPath, outSplit)))
