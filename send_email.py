from kijiji import send_email, temp_dir
from os import listdir, remove
from os.path import isfile, join
import pandas as pd


files = [f for f in listdir(temp_dir) if isfile(join(temp_dir, f))]
for file in files:
    filename = file[:-4]
    dataframe = pd.read_pickle(temp_dir + file)
    send_email(filename, dataframe)
    remove(temp_dir + file)
