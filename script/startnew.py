import os
import glob
import runpy

# delete all old db files
for i in glob.glob(r'.\data\creditcard.db'):
    os.remove(i)
for i in glob.glob(r'.\data\*.db-shm'):
    os.remove(i)
for i in glob.glob(r'.\data\*.db-wal'):
    os.remove(i)

# delete config file
for j in glob.glob(r'.\config.json'):
    os.remove(j)

# delete config file
for j in glob.glob(r'.\models\*.save'):
    os.remove(j)

# delete saved classifier model files
for j in glob.glob(r'.\models\*.h5'):
    os.remove(j)

# create new database
runpy.run_path(r'.\script\create_new_db.py')
print('Done!')

