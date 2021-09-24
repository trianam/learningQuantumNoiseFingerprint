#!/usr/bin/env python
# coding: utf-8

import numpy as np
import os
import sys
from runSvm import runSVM
import configurations


if __name__ == "__main__":
    outPath = "files"

    #==========================================================================================

    # machinePairs = [
    #     [
    #         [
    #             [['ibmq_belem'], 'D-{}-{}'.format(j+1, i+1)] for i in range(600)
    #         ], 'D{}.dat'.format(j)
    #     ] for j in range(5)
    # ]

    #==========================================================================================

    # machinePairs = [
    #     [
    #         [
    #             [['ibmq_belem'], 'E-{}-{}'.format(j+1, i+1)] for i in range(400)
    #         ], 'E{}.dat'.format(j)
    #     ] for j in range(3)
    # ]

    #==========================================================================================

    windowsEnds = [400, 800, 1200]
    machinePairs = [
        [
            [
                [['ibmq_belem'], 'F-{}-{}'.format(j+1, i+1)] for i in range(2000-(windowsEnds[j]+400))
            ], 'F{}.dat'.format(j)
        ] for j in range(3)
    ]

    #==========================================================================================

    tSeq = [0,1,2,3,4,5,6,7,8]

    for (configs, fileName) in machinePairs:
        print("Writing in {}".format(fileName))
        with open(os.path.join(outPath, fileName), 'tw') as file:
            for (machines, configName) in configs:
                currConf = configurations.configSlowCustomTemporalGen(machines, configName, tSeq)
                accuracy = runSVM(currConf)
                file.write("{}\n".format(accuracy))

