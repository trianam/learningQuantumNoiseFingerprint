#!/usr/bin/env python
# coding: utf-8

import pickle
import os
import glob
import numpy as np

repeatedMeasures = None #no repeated measures
readBits = None #read all bits

#Classification
basePath = 'data/walker'
# machines = ['ibmq_athens', 'ibmq_athens-splitA', 'ibmq_athens-splitB', 'ibmq_athens-split10A', 'ibmq_athens-split10B', 'ibmq_athens-split10C', 'ibmq_athens-split10D', 'ibmq_athens-split10E', 'ibmq_athens-split10F', 'ibmq_athens-split10G', 'ibmq_athens-split10H', 'ibmq_athens-split10I', 'ibmq_athens-split10J', 'ibmq_santiago', 'ibmq_casablanca', 'ibmq_casablanca-bis', 'ibmq_5_yorktown', 'ibmq_bogota', 'ibmq_lima', 'ibmq_quito'] #included suffix
machines = ['ibmq_athens', 'ibmq_santiago'] #included suffix
outPath = 'data/walkerExtracted'

# basePath = 'data/walkerSlow1000'
# machines = ['ibmq_belem', 'ibmq_quito']
# outPath = 'data/walkerSlow1000Extracted'

# basePath = 'data/walkerSlow1500'
# machines = ['ibmq_belem', 'ibmq_quito']
# outPath = 'data/walkerSlow1500Extracted'

# basePath = 'data/walkerSlow'
# machines = ['ibmq_belem', 'ibmq_quito']
# outPath = 'data/walkerSlowExtracted'

# basePath = 'data/walkerSimple'
# machines = ['ibmq_belem', 'ibmq_quito']
# outPath = 'data/walkerSimpleExtracted'
# readBits = [3,2]

# basePath = 'data/walkerSingleMeasures'
# machines = ['ibmq_belem', 'ibmq_quito']
# outPath = 'data/walkerSingleMeasuresExtracted'
# readBits = [3,2]
# repeatedMeasures = 10
# bitsPerMeasure = 4

#Time series ramsey
# basePath = 'data/ramsey'
# machines = ['ibmq_rome']
# outPath = 'data/ramseyExtracted'

#Time series walker
# basePath = 'data/walkerLong'
# machines = ['ibmq_bogota']
# outPath = 'data/walkerLongExtracted'


# windowSizes = [200, 1000]
windowSizes = [1000]
saveExecutions = False

os.makedirs(outPath, exist_ok=True)

for m in machines:
    executions = []
    # for filename in sorted(glob.glob(os.path.join(basePath, '{}*'.format(m))), key=lambda f:int(f.replace(os.path.join(basePath, '{}-'.format(m)), '').replace('.p', ''))): #all the files related to m, sorted by the int index (with correct progressive)
    for filename in sorted(glob.glob(os.path.join(basePath, '{}-'.format(m)+('[0-9]'*6)+'.p'))):
        print("Read ", filename)
        results = pickle.load(open(filename, 'rb'))

        for n in range(len(results['results'][0]['data']['memory'])):
            currExecution = []
            if repeatedMeasures is None:
                for t in range(len(results['results'])):
                    execution = int(results['results'][t]['data']['memory'][n], 0)
                    if not readBits is None:
                        value = 0
                        for b in readBits:
                            value = (value<<1) + ((execution >> b) & 1)
                        execution = value

                    currExecution.append(execution)
            else:
                execution = int(results['results'][0]['data']['memory'][n], 0)
                if readBits is None:
                    readBits = list(reversed(range(bitsPerMeasure)))
                for t in range(repeatedMeasures):
                    value = 0
                    for b in readBits:
                        value = (value<<1) + ((execution >> (t*bitsPerMeasure)+b) & 1)

                    currExecution.append(value)

            executions.append(currExecution)

    executions = np.array(executions)

    if saveExecutions:
        saveFile = os.path.join(outPath, 'executions-{}.csv'.format(m))
        print("Saving executions in {} with shape {}".format(saveFile, executions.shape))
        np.savetxt(saveFile, executions, delimiter=',')

    for k in windowSizes:
        if executions.shape[0] % k > 0:
            raise(Exception("Not divisible"))

        print("Calculate probabilities with k={}".format(k))
        probabilities = np.zeros((int(executions.shape[0]/k), executions.shape[1], len(np.unique(executions))), dtype='float32')
        for n in range(executions.shape[0]):
            i = int(n/k)
            for t in range(executions.shape[1]):
                probabilities[i,t,executions[n,t]] += 1

        probabilities = probabilities / k
        saveFileProb = os.path.join(outPath, 'probabilities-{}-{}.npy'.format(k,m))
        print("Saving probabilities in {} with shape {}".format(saveFileProb, probabilities.shape))
        np.save(saveFileProb, probabilities)
