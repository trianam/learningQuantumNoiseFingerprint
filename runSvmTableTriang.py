#!/usr/bin/env python
# coding: utf-8

import numpy as np
import os
import sys
from runSvm import runSVM
import configurations


if __name__ == "__main__":
    outFilename = "files/SVMtableTriang.txt"

    machines = ['ibmq_athens', 'ibmq_bogota', 'ibmq_casablanca', 'ibmq_lima', 'ibmq_quito', 'ibmq_santiago', 'ibmq_5_yorktown']
    # machines = ['ibmq_athens', 'ibmq_bogota', 'ibmq_casablanca']

    tPairs = [
        [[0], [0]],
        [[1], [0,1]],
        [[2], [0,1,2]],
        [[3], [0,1,2,3]],
        [[4], [0,1,2,3,4]],
        [[5], [0,1,2,3,4,5]],
        [[6], [0,1,2,3,4,5,6]],
        [[7], [0,1,2,3,4,5,6,7]],
        [[8], [0,1,2,3,4,5,6,7,8]],
    ]

    print("Writing in {}".format(outFilename))
    with open(outFilename, 'tw') as file:
        toWrite = "    \\begin{{tabular}}{{c|{}}}\n" \
                "        Machines {}\\\\\n" \
                "        \\hline\n".format("ccc|"*(len(machines)-1), "".join(["& \multicolumn{{3}}{{c|}}{{{}}}".format(m.split("_")[-1].capitalize()) for m in machines[:-1] ]))
        file.write(toWrite)

        numAllMachinePairs = (len(machines)*(len(machines)+1))/2
        for r in range(1,len(machines)):
            print("Calculating row {}/{} ({})\t".format(r, len(machines)-1, machines[r]), end="", flush=True)
            numMachinePair = (r*(r+1))/2
            file.write("        \\multirow{{9}}{{1.8cm}}{{{}}} ".format(machines[r].split("_")[-1].capitalize()))
            for numTPair, (tOrdCol1, tOrdCol2) in enumerate(tPairs):
                print("t {}/9\t".format(numTPair+1), end="", flush=True)
                file.write("        ")

                for c in range(0, r):
                    col1Conf = configurations.configGen([machines[c], machines[r]], tOrdCol1)
                    col2Conf = configurations.configGen([machines[c], machines[r]], tOrdCol2)

                    col1MaxAcc = runSVM(col1Conf)
                    col2MaxAcc = runSVM(col2Conf)
                    # col1MaxAcc = 0
                    # col2MaxAcc = 0

                    file.write("& ${}$ & $\\accuracy{{{:.3f}}}$ & $\\accuracy{{{:.3f}}}$ ".format(len(tOrdCol2), col1MaxAcc, col2MaxAcc))

                file.write(" & & & " * (len(machines)-r-1) + "\\\\\n")

            print("")

            file.write("        \\hline\n")

        file.write("    \\end{tabular}\n")

        print("END")
