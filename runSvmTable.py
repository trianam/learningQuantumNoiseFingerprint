#!/usr/bin/env python
# coding: utf-8

import numpy as np
import os
import sys
from runSvm import runSVM
import configurations


if __name__ == "__main__":
    outFilename = "files/SVMtable.txt"

    machinePairs = [
        # ======================================= Binary
        # [['ibmq_athens', 'ibmq_bogota'], None, None],
        # [['ibmq_athens', 'ibmq_casablanca'], None, None],
        # [['ibmq_athens', 'ibmq_lima'], None, None],
        # [['ibmq_athens', 'ibmq_quito'], None, None],
        # [['ibmq_athens', 'ibmq_santiago'], None, None],
        # [['ibmq_athens', 'ibmq_5_yorktown'], None, None],
        # [['ibmq_bogota', 'ibmq_casablanca'], None, None],
        # [['ibmq_bogota', 'ibmq_lima'], None, None],
        # [['ibmq_bogota', 'ibmq_quito'], None, None],
        # [['ibmq_bogota', 'ibmq_santiago'], None, None],
        # [['ibmq_bogota', 'ibmq_5_yorktown'], None, None],
        # [['ibmq_casablanca', 'ibmq_lima'], None, None],
        # [['ibmq_casablanca', 'ibmq_quito'], None, None],
        # [['ibmq_casablanca', 'ibmq_santiago'], None, None],
        # [['ibmq_casablanca', 'ibmq_5_yorktown'], None, None],
        # [['ibmq_lima', 'ibmq_quito'], None, None],
        # [['ibmq_lima', 'ibmq_santiago'], None, None],
        # [['ibmq_lima', 'ibmq_5_yorktown'], None, None],
        # [['ibmq_quito', 'ibmq_santiago'], None, None],
        # [['ibmq_quito', 'ibmq_5_yorktown'], None, None],
        # [['ibmq_santiago', 'ibmq_5_yorktown'], None, None],

        # ======================================= Temporal
        # [['ibmq_casablanca', 'ibmq_casablanca-bis'], None, None],

        # ======================================= Multiclass
        # [['ibmq_athens', 'ibmq_bogota', 'ibmq_casablanca', 'ibmq_lima', 'ibmq_quito', 'ibmq_santiago', 'ibmq_5_yorktown'], None, None],
        # [['ibmq_5_yorktown', 'ibmq_athens', 'ibmq_bogota', 'ibmq_casablanca', 'ibmq_santiago'], None, None],

        # ======================================= Slow temporal
        # [['ibmq_belem'], 200, None],
        # [['ibmq_belem'], 400, None],

        # ======================================= Slow temporal customTemporalDataset
        [['ibmq_belem'], None, 'A1'],
        [['ibmq_belem'], None, 'A2'],
        [['ibmq_belem'], None, 'A3'],
        [['ibmq_belem'], None, 'A4'],
        [['ibmq_belem'], None, 'A5'],
        [['ibmq_belem'], None, 'A6'],
        [['ibmq_belem'], None, 'A7'],
        [['ibmq_belem'], None, 'A8'],
        [['ibmq_belem'], None, 'A9'],

    ]

    titleBase = "Machines & $k$ & Acc. ($k$) & Acc ($1,\\dots,k$)\\\\"
    tSeqBase = [
        [[0],    [0]],
        [[1],    [0,1]],
        [[2],    [0,1,2]],
        [[3],    [0,1,2,3]],
        [[4],    [0,1,2,3,4]],
        [[5],    [0,1,2,3,4,5]],
        [[6],    [0,1,2,3,4,5,6]],
        [[7],    [0,1,2,3,4,5,6,7]],
        [[8],    [0,1,2,3,4,5,6,7,8]],
    ]

    titleExt = "Machines & $k$ & $\\alpha(k)$ & $\\alpha([k\mathrm{-}1,k])$ & $\\alpha([k\mathrm{-}2,k])$ & $\\alpha([k\mathrm{-}3,k])$ & $\\alpha([k\mathrm{-}4,k])$ & $\\alpha([1,k])$ & $\\alpha([p_1,p_k])$\\\\"
    tSeqExt = [
        [[0],   [],     [],         [],         [],             [0],                    [0]],
        [[1],   [0,1],  [],         [],         [],             [0,1],                  [0,8]],
        [[2],   [1,2],  [0,1,2],    [],         [],             [0,1,2],                [0,8,4]],
        [[3],   [2,3],  [1,2,3],    [0,1,2,3],  [],             [0,1,2,3],              [0,8,4,2]],
        [[4],   [3,4],  [2,3,4],    [1,2,3,4],  [0,1,2,3,4],    [0,1,2,3,4],            [0,8,4,2,6]],
        [[5],   [4,5],  [3,4,5],    [2,3,4,5],  [1,2,3,4,5],    [0,1,2,3,4,5],          [0,8,4,2,6,1]],
        [[6],   [5,6],  [4,5,6],    [3,4,5,6],  [2,3,4,5,6],    [0,1,2,3,4,5,6],        [0,8,4,2,6,1,3]],
        [[7],   [6,7],  [5,6,7],    [4,5,6,7],  [3,4,5,6,7],    [0,1,2,3,4,5,6,7],      [0,8,4,2,6,1,3,5]],
        [[8],   [7,8],  [6,7,8],    [5,6,7,8],  [4,5,6,7,8],    [0,1,2,3,4,5,6,7,8],    [0,8,4,2,6,1,3,5,7]],
    ]

    titleExt2 = "Machines & $k$ & $\\alpha(k)$ & $\\alpha(k\mathrm{-}1,k)$ & $\\alpha(k\mathrm{-}2,k)$ & $\\alpha(k\mathrm{-}3,k)$ & $\\alpha(k\mathrm{-}4,k)$ & $\\alpha([1,k])$ & $\\alpha([p_1,p_k])$\\\\"
    tSeqExt2 = [
        [[0],   [],     [],       [],     [],       [0],                    [0]],
        [[1],   [0,1],  [],       [],     [],       [0,1],                  [0,8]],
        [[2],   [1,2],  [0,2],    [],     [],       [0,1,2],                [0,8,4]],
        [[3],   [2,3],  [1,3],    [0,3],  [],       [0,1,2,3],              [0,8,4,2]],
        [[4],   [3,4],  [2,4],    [1,4],  [0,4],    [0,1,2,3,4],            [0,8,4,2,6]],
        [[5],   [4,5],  [3,5],    [2,5],  [1,5],    [0,1,2,3,4,5],          [0,8,4,2,6,1]],
        [[6],   [5,6],  [4,6],    [3,6],  [2,6],    [0,1,2,3,4,5,6],        [0,8,4,2,6,1,3]],
        [[7],   [6,7],  [5,7],    [4,7],  [3,7],    [0,1,2,3,4,5,6,7],      [0,8,4,2,6,1,3,5]],
        [[8],   [7,8],  [6,8],    [5,8],  [4,8],    [0,1,2,3,4,5,6,7,8],    [0,8,4,2,6,1,3,5,7]],
    ]

    titleRandPerm = "Machines & $k$ & $\\alpha(k\mathrm{-}1,k)$ & $\\alpha(p_k\mathrm{-}1,p_k)$ & $\\alpha(q_k\mathrm{-}1,q_k)$ & $\\alpha(r_k\mathrm{-}1,r_k)$ & $\\alpha(s_k\mathrm{-}1,s_k)$ & $\\alpha(u_k\mathrm{-}1,u_k)$\\\\"
    tSeqRandPerm = [
        [[],     [],     [],     [],     [],    []],
        [[0,1],  [2,6],  [0,6],  [3,0],  [7,3], [7,1]],
        [[1,2],  [6,8],  [6,1],  [0,7],  [3,5], [1,2]],
        [[2,3],  [8,5],  [1,4],  [7,2],  [5,4], [2,6]],
        [[3,4],  [5,0],  [4,7],  [2,4],  [4,0], [6,0]],
        [[4,5],  [0,4],  [7,8],  [4,8],  [0,2], [0,8]],
        [[5,6],  [4,7],  [8,2],  [8,5],  [2,8], [8,4]],
        [[6,7],  [7,3],  [2,5],  [5,6],  [8,1], [4,5]],
        [[7,8],  [3,1],  [5,3],  [6,1],  [1,6], [5,3]],
    ]

    tSeq, title = tSeqBase, titleBase
    # tSeq, title = tSeqExt, titleExt
    # tSeq, title = tSeqExt2, titleExt2
    # tSeq, title = tSeqRandPerm, titleRandPerm

    printAverages = False

    print("Writing in {}".format(outFilename))
    with open(outFilename, 'tw') as file:
        toWrite = "    \\begin{tabular}{c|c|"+"|".join(["c" for _ in range(len(tSeq[0]))])+"}\n" \
                "        "+title+"\n" \
                "        \\hline\n"
        file.write(toWrite)

        for numMachinePair, (machines, temporal, customTemporal) in enumerate(machinePairs):
            toWrite = "        \\multirow{{9}}{{2cm}}{{{}}} ".format(' \&\,\,'.join([ m.split('_')[-1].capitalize() for m in machines]))
            file.write(toWrite)
            maxAccuracies = []
            for numTSeq, currTSeq in enumerate(tSeq):
                print("Calculating {} ({}/{}, {}%)                   ".format('-'.join(machines), numMachinePair+1, len(machinePairs), int(numTSeq/(len(tSeq)-1)*100)), end='\r', flush=True)
                currAccuracies = []
                for tOrd in currTSeq:
                    if not temporal is None:
                        currConf = configurations.configSlowTemporalGen(machines, temporal, tOrd)
                    elif not customTemporal is None:
                        currConf = configurations.configSlowCustomTemporalGen(machines, customTemporal, tOrd)
                    else:
                        currConf = configurations.configGen(machines, tOrd)
                    if len(tOrd) != 0:
                        currAccuracies.append(runSVM(currConf))
                    else:
                        currAccuracies.append(None)
                maxAccuracies.append(currAccuracies)

            print("")

            averages = np.zeros(len(maxAccuracies[0]))
            averagesNum = np.zeros(len(maxAccuracies[0]))
            for t, currAccuracies in enumerate(maxAccuracies):
                for i,c in enumerate(currAccuracies):
                    if not c is None:
                        averages[i] += c
                        averagesNum[i] += 1
                toWrite = "& ${}$ {} \\\\\n        ".format(t+1, " ".join(["& $\\accuracy{{{:.3f}}}$".format(acc) if not acc is None else "&" for acc in currAccuracies]))
                file.write(toWrite)

            averages = averages / averagesNum
            toWrite = "\\hline\n"
            file.write(toWrite)
            if printAverages:
                toWrite = "Average& & {} \\\\\n        ".format(" & ".join(["$\\accuracy{{{:.3f}}}$".format(avg) for avg in averages]))
                file.write(toWrite)
                toWrite = "\\hline\n"
                file.write(toWrite)

        toWrite = "    \\end{tabular}\n"
        file.write(toWrite)
