#!/usr/bin/env python
# coding: utf-8

# Importing standard Qiskit libraries and configuring account
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *

import pickle
import os
import numpy as np
import time
from datetime import datetime
from multiprocessing import Process, Lock, Manager

# circuitType = "walker"
circuitType = "walkerSimple"
# circuitType = "walkerSingleMeasures"
# circuitType = "ramsey"

# basePath = "data/walker"
basePath = "data/walkerSimple"
# basePath = "data/walkerSingleMeasures"
# basePath = "data/walkerLong"
# basePath = "data/walkerLore"
# basePath = "data/walkerSte"
# basePath = "data/ramsey"
# basePath = "data/walkerSlow"

firstStep = 1
# steps = 9 # for walker
# steps = 10 # for ramsey
steps = 10 # for walkerSimple
# firstStep = 5
# steps = 1  # for walkerSingleMeasures

#runs for each backend (all backends in parallel)
# runs = 1
runs = 250
# runs = 1250 #check ulimit -Sn 100000; ulimit -a
# runs = 1000 #check ulimit -Sn 100000; ulimit -a
# runs = 2500 #check ulimit -Sn 100000; ulimit -a
# runs = 20

shots = 8000
# shots = 1000

#concurrent processes for each backend (all backends in parallel)
# concurrentJobs = 20 #for researchers
concurrentJobs = 5  #for open
# concurrentJobs = 1

minWaitSecs = None #better None with more than 1 concurrentJobs
# minWaitSecs = 120

backends = [
    'ibmq_qasm_simulator',
    'ibmq_qasm_simulator',
    # 'ibmq_athens',
    # 'ibmq_santiago',
    # 'ibmq_casablanca',
    # 'ibmq_bogota',
    # 'ibmq_rome',
    # 'ibmq_lima',
    # 'ibmq_quito',
    # 'ibmq_5_yorktown',
    # 'ibmq_belem',
]

progressiveStart = 1
progressiveFileStart = 1
# progressiveFileStart = 1001

user = 'Stefano Martina'
project = circuitType.lower()[:16] #standard naming
# project = 'walkerslow'

# user = 'Lorenzo Buffoni'
# user = 'Stefano Gherardini'

suffix = ""
# suffix = "-bis"

users = {
    'Stefano Martina' : {
        'token' : 'OMISSIS',
        'hub' : 'OMISSIS',
        'group' : 'OMISSIS',
        'project' : 'OMISSIS',
    },
    'Lorenzo Buffoni' : {
        'token' : 'OMISSIS',
        'hub' : 'OMISSIS',
        'group' : 'OMISSIS',
        'project' : 'OMISSIS',
    },
    'Stefano Gherardini' : {
        'token' : 'OMISSIS',
        'hub' : 'OMISSIS',
        'group' : 'OMISSIS',
        'project' : 'OMISSIS',
    },
}


def walker(step):
    circ = QuantumCircuit(4, 4)
    for i in range(step):
        if i%3 == 0:
            circ.h(0)
            circ.h(1)
            circ.cx(0,2)

            circ.barrier(0,1,2,3)
        elif i%3 ==1:
            circ.cx(1,3)
            circ.x(0)

            circ.barrier(0,1,2,3)
        else:
            circ.x(1)
            circ.ccx(0,1,2)

            circ.barrier(0,1,2,3)
    circ.measure(2, 0)
    circ.measure(3, 1)

    return circ

def walkerSimple(step):
    circ = QuantumCircuit(4, 4)
    for i in range(step):
        if i%2 == 0:
            circ.h(0)
            circ.cx(0,2)
            circ.barrier(0,1,2,3)
        else:
            circ.h(1)
            circ.cx(1,3)
            circ.barrier(0,1,2,3)

    for q in range(len(circ.qubits)):
        circ.measure(q, q)

    return circ

def walkerSingleMeasures(step): #meant to be used with firstStep=k and steps = 1
    numCubits = 4
    circ = QuantumCircuit(numCubits, step*numCubits*2)
    for i in range(step):
        circ.h(0)
        circ.cx(0,2)

        circ.barrier(range(numCubits))
        for q in range(numCubits):
            circ.measure(q, (i*numCubits*2)+q)
        circ.barrier(range(numCubits))

        circ.h(1)
        circ.cx(1,3)

        circ.barrier(range(numCubits))
        for q in range(numCubits):
            circ.measure(q, (i*numCubits*2)+numCubits+q)
        circ.barrier(range(numCubits))

    return circ

def ramsey(step):
    circ = QuantumCircuit(1, 1)
    circ.h(0)
    circ.barrier(0)
    circ.s(0)
    for i in range(step):
        circ.x(0)
        circ.s(0)
        circ.barrier(0)
    circ.h(0)
    circ.barrier(0)

    circ.measure(0, 0)
    return circ


def run(circs, provider, backend="ibmq_qasm_simulator", shots=8000, memory=True):
    backendObj = provider.backends(backend)[0] # change backends
    job = execute(circs, backendObj, shots=shots, memory=memory) # change number of shots
    result = job.result()

    return result

    #counts = result.get_counts(circs) # We obtain the frequency of each result and we show them
    #toReturn = counts

    #if memory:
    #    executions = result.get_memory()
    #    toReturn = [toReturn, executions]
    
    #return toReturn

def proc(lock, control, minWaitSecs, provider, backend, circs, shots, basePath, suffix):
    busy = True
    while busy:
        lock.acquire()
        try:
            if control['free'] > 0:
                #minWaitSecs doesn't make too much sense with many parallel processes
                if minWaitSecs is None or not 'lastEndTime' in control or (datetime.now() - control['lastEndTime']).seconds >= minWaitSecs:
                    control['free'] -= 1
                    busy = False
        finally:
            lock.release()
        if busy:
            time.sleep(1)

    lock.acquire()
    try:
        p = control['progressive']
        control['progressive'] += 1
        startTime = datetime.now()
        print("{} - Start {} {}".format(startTime.strftime("%d/%m/%Y %H:%M:%S"), backend, p))
    finally:
        lock.release()

    errors = True
    while errors: #retry indefinitely if errors
        errors = False
        try:
            resultQ = run(circs, provider=provider, backend=backend, shots=shots)
        except Exception as e:
            print(e)
            print("Retry in 10 seconds")
            time.sleep(10)
            errors = True


    lock.acquire()
    try:
        pf = control['progressiveFile']
        control['progressiveFile'] += 1
        filenameQ = os.path.join(basePath,"{}{}-{:06d}.p".format(backend, suffix, pf)) #use different progressive to keep the run order

        dictQ = resultQ.to_dict()
        pickle.dump(dictQ, open(filenameQ, 'wb'))

        endTime = datetime.now()
        print("{} ({}) - End {} {} ({})".format(endTime.strftime("%d/%m/%Y %H:%M:%S"), str(endTime-startTime).split('.', 2)[0], backend, p, filenameQ))
        control['lastEndTime'] = endTime
        control['free'] += 1
    finally:
        lock.release()

def draw(drawStep):
    circs = []
    for step in range(firstStep, firstStep + steps):
        circ = eval(circuitType + "(step)")
        circs.append(circ)

    circs[drawStep-1].draw(output='mpl')

def getCircs():
    circs = []
    for step in range(firstStep, firstStep + steps):
        circ = eval(circuitType + "(step)")
        circs.append(circ)

    return circs

if __name__ == "__main__":

    startTime = datetime.now()
    os.makedirs(basePath, exist_ok=True)

    print("Load {} account".format(user))
    # Loading your IBM Q account(s)
    IBMQ.enable_account(users[user]['token'])
    for p in IBMQ.providers():
        print(p)
    provider = IBMQ.get_provider(hub=users[user]['hub'], group=users[user]['group'], project=users[user]['project'])

    print("Build circuit {} with {} steps".format(circuitType, steps))
    circs = []
    for step in range(firstStep,firstStep+steps):
        circ = eval(circuitType+"(step)")
        circs.append(circ)


    with Manager() as manager:
        lock = Lock()
        processes = []
        controls = []

        for backend in backends:
            print("Run {} runs on {}".format(runs, backend), end = "")
            controls.append(manager.dict({'free': concurrentJobs, 'progressive': progressiveStart, 'progressiveFile': progressiveFileStart}))
            for _ in range(runs):
                processes.append(Process(target=proc, args=(lock, controls[-1], minWaitSecs, provider, backend, circs, shots, basePath, suffix)))
                processes[-1].start()
                print(".", end="")
            print(";")

        # with Pool(runs) as p:
        #     p.starmap(proc, [(r, backend, circs, shots) for r in range(runs)])

        # for r in range(runs):
        #     print("{} - Run {}/{}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), r+1, runs), end="")
        #
        #     resultQ = run(circs, useBackend=backend, shots=shots)
        #     dictQ = resultQ.to_dict()
        #
        #     filenameQ = "{}-{}.p".format(backend, r)
        #     print(" - Saved in ", os.path.join(basePath,filenameQ))
        #     pickle.dump(dictQ, open(os.path.join(basePath,filenameQ), 'wb'))

        for p in processes:
            p.join()

    endTime = datetime.now()
    print("{} - End All ({})".format(endTime.strftime("%d/%m/%Y %H:%M:%S"), str(endTime-startTime).split('.', 2)[0]))
