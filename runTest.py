import os

os.system("python extractExecutions.py")
os.system("python createDataset.py")
os.system("python runSvm.py config2t")
