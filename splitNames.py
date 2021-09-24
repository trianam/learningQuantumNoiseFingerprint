import os
import glob
import string

basePath = 'files/walker'
machine = 'ibmq_athens'
splits = 10
prefix = "split10"

files = sorted(glob.glob(os.path.join(basePath, '{}-'.format(machine)+('[0-9]'*6)+'.p')))

f = 0
for s in range(splits):
    prog = 1
    for _ in range(int(len(files)/splits)):
        newFilename = os.path.join(basePath, "{}-{}{}-{:06d}.p".format(machine, prefix, string.ascii_uppercase[s], prog))
        prog += 1
        print("{} -> {}".format(files[f], newFilename))
        os.symlink(os.path.basename(files[f]), newFilename)
        f += 1
