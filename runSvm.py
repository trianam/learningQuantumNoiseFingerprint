#!/usr/bin/env python
# coding: utf-8

from sklearn import svm
from sklearn import preprocessing
import numpy as np
import os
import sys
import configurations


def extractData(conf, verbose, normalize=False):
    if verbose:
        print("Dataset: {}".format(conf.dataset))
        print("Split: {}".format(conf.split))
        print("Normalization: {}".format(normalize))

    fileDataset = np.load(os.path.join('data', conf.dataset))
    fileSplit = np.load(os.path.join('data', conf.split))

    data = {k:{} for k in fileSplit.keys()}

    x = fileDataset['x']
    y = fileDataset['y']

    for ik,k in enumerate(fileSplit.keys()):
        split = fileSplit[k]
        #split = [i for s in [fileSplit[k] for k in fileSplit] for i in s]

        #debug
        # split = split[:1000]

        data[k]['x'] = x[split]
        if conf.tOrd != list(range(data[k]['x'].shape[1])):
            if ik == 0 and verbose:
                print("Takes only T {} out of 0:{}".format(" ".join(map(str,conf.tOrd)), data[k]['x'].shape[1]))
            data[k]['x'] = data[k]['x'][:,conf.tOrd,:]
        # if takeN is None:
        #     data[k]['x'] = data[k]['x'].reshape(data[k]['x'].shape[0],-1) #take all
        # else:
        #     data[k]['x'] = data[k]['x'][:,takeN,:]
        data[k]['x'] = data[k]['x'].reshape(data[k]['x'].shape[0],-1) #concatenate all
        data[k]['y'] = y[split]

    if normalize == 'meanStd':
        trainMean = data['train']['x'].mean(axis=0)
        trainStd = data['train']['x'].std(axis=0)
        for k in data:
            data[k]['x'] = (data[k]['x'] - trainMean) / trainStd

    elif normalize == 'minMax':
        trainMin = np.min(data['train']['x'])
        trainMax = np.max(data['train']['x'])
        for k in data:
            data[k]['x'] = (data[k]['x'] - trainMin) / (trainMax - trainMin)

    elif normalize == 'standardScaler':
        scaler = preprocessing.StandardScaler().fit(data['train']['x'])
        for k in data:
            data[k]['x'] = scaler.transform(data[k]['x'])

    elif normalize is not False:
        raise ValueError("normalizeP not valid")

    return data

def train(clf, data):
    clf.fit(data['train']['x'], data['train']['y'])

    pred = {k:clf.predict(data[k]['x']) for k in data.keys()}
    acc = {k: np.sum(pred[k] == data[k]['y']) / len(data[k]['y']) for k in data.keys()}
    return acc



def runSVM(conf, mask = [True]*6, verbose=False, writeToFile=False):
    # normalize = "meanStd"
    # normalize = "minMax"
    # normalize = "standardScaler"
    normalize = False

    data = extractData(conf, verbose, normalize)

    outPath = os.path.join('files', conf.path, 'svm')
    if writeToFile:
        os.makedirs(outPath, exist_ok=True)
        # outFilename =  os.path.join(outPath, 'results{}_{}.txt'.format("_"+normalize if normalize else "", takeN if not takeN is None else "all"))
        outFilename =  os.path.join(outPath, 'results{}.txt'.format("_"+normalize if normalize else ""))
        if verbose:
            print("Saving in {}".format(outFilename))

    if writeToFile:
        file = open(outFilename, 'tw')

    maxValidAcc = -1
    maxTestAcc = -1
    maxKernel = ""
    for algNum,(algName, algFun) in enumerate([
        ["Linear SVM (LinearSVC)", svm.LinearSVC()],
        ["Linear SVM", svm.SVC(kernel='linear', decision_function_shape='ovr')],
        ["Poly d.2 SVM", svm.SVC(kernel='poly', degree=2, decision_function_shape='ovr')],
        ["Poly d.3 SVM", svm.SVC(kernel='poly', degree=3, decision_function_shape='ovr')],
        ["Poly d.4 SVM", svm.SVC(kernel='poly', degree=4, decision_function_shape='ovr')],
        ["RBF SVM", svm.SVC(kernel='rbf', decision_function_shape='ovr')],
    ]):
        if mask[algNum]:
            acc = train(algFun, data)
            toPrint = "\n{}:\nTrain acc.: {}; valid acc.: {}; test acc.: {}\n".format(algName, acc['train'], acc['valid'], acc['test'])
            if verbose:
                print(toPrint, end='')
            if writeToFile:
                file.write(toPrint)
            if acc['valid'] > maxValidAcc:
                maxValidAcc = acc['valid']
                maxTestAcc = acc['test']
                maxKernel = algName

    toPrint = "\n=============================================\nBetter valid: {}; test acc.: {} ({:.1f}%)\n".format(maxKernel, maxTestAcc, maxTestAcc*100)
    if verbose:
        print(toPrint, end='')
    if writeToFile:
        file.write(toPrint)
        file.close()

    return(maxTestAcc)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use {} configName [mask (t|f*6)]".format(sys.argv[0]))
    else:
        conf = getattr(sys.modules['configurations'], sys.argv[1])

        if len(sys.argv) > 2:
            if len(sys.argv[2]) != 6:
                raise ValueError("Use sequence of 6 elements.")

            mask = []
            for v in sys.argv[2]:
                if v == 't':
                    mask.append(True)
                elif v == 'f':
                    mask.append(False)
                else:
                    raise ValueError("Use sequence of 't' and 'f'.")
        else:
            mask = [True]*6

        _ = runSVM(conf, mask, verbose=True, writeToFile=True)
