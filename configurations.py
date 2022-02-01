#     tuneConfigurations.py
#     The configurations for all the experiments.
#     Copyright (C) 2021  Stefano Martina (stefano.martina@unifi.it)
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from conf import Conf
import numpy as np

configGlobal = Conf({
})


config1t = configGlobal.copy({
    "path":                 'config1t',
    "dataset":              'walker-dataset-ibmq_casablanca-ibmq_santiago-1000.npz',
    "split":                'walker-split-ibmq_casablanca-ibmq_santiago-1000.npz',
    "tOrd":                 [0,1],
})

config2t = configGlobal.copy({
    "path":                 'config2t',
    "dataset":              'walker-dataset-ibmq_athens-ibmq_santiago-1000.npz',
    "split":                'walker-split-ibmq_athens-ibmq_santiago-1000.npz',
    "tOrd":                 [0],
})

config3t = configGlobal.copy({
    "path":                 'config3t',
    "dataset":              'walker-dataset-ibmq_casablanca-ibmq_casablanca-bis-1000.npz',
    "split":                'walker-split-ibmq_casablanca-ibmq_casablanca-bis-1000.npz',
})

config4t = configGlobal.copy({
    "path":                 'config4t',
    "useTune":              False,
    "nonVerbose":           False,
    "dataset":              'walker-dataset-ibmq_casablanca-ibmq_casablanca-1000.npz',
    "split":                'walker-split-ibmq_casablanca-ibmq_casablanca-1000.npz',
})

config5t = configGlobal.copy({
    "path":                 'config5t',
    "useTune":              False,
    "nonVerbose":           False,
    "dataset":              'walker-dataset-ibmq_athens-splitA-ibmq_athens-splitB-1000.npz',
    "split":                'walker-split-ibmq_athens-splitA-ibmq_athens-splitB-1000.npz',
})

# ================================================ all datasets
def configGen(machines, tOrd):
    return configGlobal.copy({
        "path":                 'config1Gen-{}-{}'.format('-'.join(machines), "-".join(map(str,tOrd))),
        "dataset":              'walker-dataset-{}-1000.npz'.format('-'.join(machines)),
        "split":                'walker-split-{}-1000.npz'.format('-'.join(machines)),
        "tOrd":                 tOrd,
    })

# ================================================ different times

config1times = configGlobal.copy({
    "path":                 'config1times',
    "dataset":              'walker-dataset-ibmq_5_yorktown-ibmq_casablanca-1000-noShuffle.npz',
    "split":                'walker-split-ibmq_5_yorktown-ibmq_casablanca-1000-noShuffle-25.npz',
})

# ================================================ slow walker

config1slow1000 = configGlobal.copy({
    "path":                 'config1slow1000',
    "dataset":              'walkerSlow1000-dataset-ibmq_belem-ibmq_quito-1000-noShuffle.npz',
    "split":                'walkerSlow1000-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter.npz',
})

config2slow1000 = config1slow1000.copy({
    "path":                 'config2slow1000',
    "tOrd":                 [0,1],
})

config3slow1000 = config1slow1000.copy({
    "path":                 'config3slow1000',
    "split":                'walkerSlow1000-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitA.npz',
})

config4slow1000 = config1slow1000.copy({
    "path":                 'config4slow1000',
    "split":                'walkerSlow1000-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitB.npz',
})

#--------

config1slow1500 = config1slow1000.copy({
    "path":                 'config1slow1500',
    "dataset":              'walkerSlow1500-dataset-ibmq_belem-ibmq_quito-1000-noShuffle.npz',
    "split":                'walkerSlow1500-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitC1.npz',
})

config2slow1500 = config1slow1000.copy({
    "path":                 'config2slow1500',
    "dataset":              'walkerSlow1500-dataset-ibmq_belem-ibmq_quito-1000-noShuffle.npz',
    "split":                'walkerSlow1500-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitC2.npz',
})

config3slow1500 = config1slow1000.copy({
    "path":                 'config3slow1500',
    "dataset":              'walkerSlow1500-dataset-ibmq_belem-ibmq_quito-1000-noShuffle.npz',
    "split":                'walkerSlow1500-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitC3.npz',
})

#-------

config1slow = config1slow1000.copy({
    "path":                 'config1slow',
    "dataset":              'walkerSlow-dataset-ibmq_belem-ibmq_quito-1000-noShuffle.npz',
    "split":                'walkerSlow-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitC1.npz',
})

config2slow = config1slow1000.copy({
    "path":                 'config2slow1500',
    "dataset":              'walkerSlow-dataset-ibmq_belem-ibmq_quito-1000-noShuffle.npz',
    "split":                'walkerSlow-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitC2.npz',
})

config3slow = config1slow1000.copy({
    "path":                 'config3slow',
    "dataset":              'walkerSlow-dataset-ibmq_belem-ibmq_quito-1000-noShuffle.npz',
    "split":                'walkerSlow-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitC3.npz',
})

config4slow = config1slow1000.copy({
    "path":                 'config4slow',
    "dataset":              'walkerSlow-dataset-ibmq_belem-ibmq_quito-1000-noShuffle.npz',
    "split":                'walkerSlow-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitC4.npz',
})

config5slow = config1slow1000.copy({
    "path":                 'config5slow',
    "dataset":              'walkerSlow-dataset-ibmq_belem-ibmq_quito-1000-noShuffle.npz',
    "split":                'walkerSlow-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitC5.npz',
})

#-------

for n in range(1,6):
    for l in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
        globals()["configSlowC{}{}".format(n,l)] = config1slow1000.copy({
            "path":                 'configSlowC{}{}'.format(n,l),
            "dataset":              'walkerSlow-dataset-ibmq_belem-ibmq_quito-1000-noShuffle.npz',
            "split":                'walkerSlow-split-ibmq_belem-ibmq_quito-1000-noShuffle-shuffleAfter-customSplitC{}{}.npz'.format(n,l),
        })

# ================================================ slow walker temporal

def configSlowTemporalGen(machines, temporal, tOrd):
    return configGlobal.copy({
        "path":                 'config1SlowTemporalGen-{}-{}-{}'.format('-'.join(machines), temporal, "-".join(map(str,tOrd))),
        "dataset":              'walkerSlowTemporal-dataset-{}-1000-temporal{}.npz'.format('-'.join(machines), temporal),
        "split":                'walkerSlowTemporal-split-{}-1000-temporal{}.npz'.format('-'.join(machines), temporal),
        "tOrd":                 tOrd,
    })

# ================================================ slow walker custom temporal

def configSlowCustomTemporalGen(machines, customTemporal, tOrd):
    return configGlobal.copy({
        "path":                 'config1SlowCustomTemporalGen-{}-{}-{}'.format('-'.join(machines), customTemporal, "-".join(map(str,tOrd))),
        "dataset":              'walkerSlowTemporal-dataset-{}-1000-customTemporal{}.npz'.format('-'.join(machines), customTemporal),
        "split":                'walkerSlowTemporal-split-{}-1000-customTemporal{}.npz'.format('-'.join(machines), customTemporal),
        "tOrd":                 tOrd,
    })

# ================================================ simple walker

configSimple1 = configGlobal.copy({
    "path":                 'configSimple1',
    "tOrd":                 [0],
    "dataset":              'walkerSimple-dataset-ibmq_belem-ibmq_quito-1000.npz',
    "split":                'walkerSimple-split-ibmq_belem-ibmq_quito-1000.npz',
})

# ================================================ single measures walker

configSingleMeasures1 = configGlobal.copy({
    "path":                 'configSingleMeasures1',
    "tOrd":                 [0],
    "dataset":              'walkerSingleMeasures-dataset-ibmq_belem-ibmq_quito-1000.npz',
    "split":                'walkerSingleMeasures-split-ibmq_belem-ibmq_quito-1000.npz',
})


# ================================================ split

configS1 = configGlobal.copy({
    "path":                 'configS1',
    "dataset":              'walker-dataset-ibmq_athens-split10A-ibmq_athens-split10B-1000.npz',
    "split":                'walker-split-ibmq_athens-split10A-ibmq_athens-split10B-1000.npz',
})

configS2 = configGlobal.copy({
    "path":                 'configS2',
    "dataset":              'walker-dataset-ibmq_athens-split10A-ibmq_athens-split10C-1000.npz',
    "split":                'walker-split-ibmq_athens-split10A-ibmq_athens-split10C-1000.npz',
})

configS3 = configGlobal.copy({
    "path":                 'configS3',
    "dataset":              'walker-dataset-ibmq_athens-split10A-ibmq_athens-split10D-1000.npz',
    "split":                'walker-split-ibmq_athens-split10A-ibmq_athens-split10D-1000.npz',
})

configS4 = configGlobal.copy({
    "path":                 'configS4',
    "dataset":              'walker-dataset-ibmq_athens-split10A-ibmq_athens-split10E-1000.npz',
    "split":                'walker-split-ibmq_athens-split10A-ibmq_athens-split10E-1000.npz',
})

configS5 = configGlobal.copy({
    "path":                 'configS5',
    "dataset":              'walker-dataset-ibmq_athens-split10A-ibmq_athens-split10F-1000.npz',
    "split":                'walker-split-ibmq_athens-split10A-ibmq_athens-split10F-1000.npz',
})

configS6 = configGlobal.copy({
    "path":                 'configS6',
    "dataset":              'walker-dataset-ibmq_athens-split10A-ibmq_athens-split10G-1000.npz',
    "split":                'walker-split-ibmq_athens-split10A-ibmq_athens-split10G-1000.npz',
})

configS7 = configGlobal.copy({
    "path":                 'configS7',
    "dataset":              'walker-dataset-ibmq_athens-split10A-ibmq_athens-split10H-1000.npz',
    "split":                'walker-split-ibmq_athens-split10A-ibmq_athens-split10H-1000.npz',
})

configS8 = configGlobal.copy({
    "path":                 'configS8',
    "dataset":              'walker-dataset-ibmq_athens-split10A-ibmq_athens-split10I-1000.npz',
    "split":                'walker-split-ibmq_athens-split10A-ibmq_athens-split10I-1000.npz',
})

configS9 = configGlobal.copy({
    "path":                 'configS9',
    "dataset":              'walker-dataset-ibmq_athens-split10A-ibmq_athens-split10J-1000.npz',
    "split":                'walker-split-ibmq_athens-split10A-ibmq_athens-split10J-1000.npz',
})

# ================================================ Multiclass

configM1 = configGlobal.copy({
    "path":                 'configM1',
    "dataset":              'walker-dataset-ibmq_5_yorktown-ibmq_athens-ibmq_bogota-ibmq_casablanca-ibmq_santiago-1000.npz',
    "split":                'walker-split-ibmq_5_yorktown-ibmq_athens-ibmq_bogota-ibmq_casablanca-ibmq_santiago-1000.npz',
})

# ================================================ Multiclass no Shuffle

configMns1 = configM1.copy({
    "path":                 'configMns1',
    "dataset":              'walker-dataset-ibmq_5_yorktown-ibmq_athens-ibmq_bogota-ibmq_casablanca-ibmq_santiago-1000-noShuffle.npz',
    "split":                'walker-split-ibmq_5_yorktown-ibmq_athens-ibmq_bogota-ibmq_casablanca-ibmq_santiago-1000-noShuffle.npz',
})

# ================================================ Multiclass short

configMS1 = configGlobal.copy({
    "path":                 'configMS1',
    "tOrd":                 [0,1,2],
    "dataset":              'walker-dataset-ibmq_5_yorktown-ibmq_athens-ibmq_bogota-ibmq_casablanca-ibmq_santiago-1000.npz',
    "split":                'walker-split-ibmq_5_yorktown-ibmq_athens-ibmq_bogota-ibmq_casablanca-ibmq_santiago-1000.npz',
})

configMS2 = configMS1.copy({
    "path":                 'configMS2',
    "tOrd":                 [0,1],
})

configMS3 = configMS1.copy({
    "path":                 'configMS3',
    "tOrd":                 [0],
})

