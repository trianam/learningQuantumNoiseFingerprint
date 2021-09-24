# learningQuantumNoiseFingerprint
Data and code for the paper: [arXiv:2109.11405](https://arxiv.org/abs/2109.11405)

**Learning the noise fingerprint of quantum devices**

Abstract:

*Noise  sources  unavoidably  affect  any  quantum  technological  device. Noise's  main  features  are  expected  to  strictly  depend  on  the  physical platform on which the quantum device is realized, in the form of a distinguishable  fingerprint.  Noise  sources  are  also  expected  to  evolve  and change over time. Here, we first identify and then characterize experimentally the noise fingerprint of IBM cloud-available quantum computers, by resorting to machine learning techniques designed to classify noise distributions using time-ordered sequences of measured outcome probabilities.*

## Instructions
* `createCircuit.py` is used to run in parallel the calls to the IBM framework to get the data that is stored in the folder `data`. ***In this repository you already find the retrieved data***.
* `extractExecutions.py`is used to process the memory saved in the previous step and get the outcome probabilities. 
* `createDataset.py` and `createDatasetTimeSeries.py` are used to arrange the runs in classification datasets.
* `conf.py` and `configurations.py` define the configurations that are used during the training of the ML models.
* `runSvm.py` contains the main functions that implement the creation, training and optimization of the Support Vector Machine models.
* `runSvmTable.py`, `runSvmTableHoriz.py` and `runSvmTableTriang.py` are scripts that create the models, train them and create the latex tables to be used in the paper.
* `calculateSlidingWindowTimeDat.ipynb` is used to create the datapoints for the figure on sliding window.
* `plotDates.ipynb` is used to create the datapoints for the figure on slow dataset times.