import os
import mne
import pandas as pd
import datetime
from config import config

def read_edf(file):
    raw_data = mne.io.read_raw_edf(file, preload=True, encoding='latin1').load_data()
    return raw_data