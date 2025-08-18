import tempfile
import numpy as np

import pandas as pd
import pywt
import mne

from src.constants import anodo_eeg_1, catodo_eeg_1, channels_names_1, anodo_eeg_2, catodo_eeg_2, channels_names_2,feature_columns
from src.utils import to_seconds


def read_edf(file):

    raw_data = mne.io.read_raw_edf(file, preload=True, encoding='latin1').load_data()
    
    try:
        raw_data = mne.set_bipolar_reference(raw_data, anodo_eeg_1, catodo_eeg_1, channels_names_1, verbose=False)
        raw_data.pick_channels(channels_names_1, verbose=False)
    except ValueError:
        raw_data = mne.set_bipolar_reference(raw_data, anodo_eeg_2, catodo_eeg_2, channels_names_2, verbose=False)
        raw_data.pick_channels(channels_names_2, verbose=False)

    exam_start_time = to_seconds(raw_data.info.get('meas_date').time())

    data = raw_data.to_data_frame()

    data['time'] = data['time'] + exam_start_time

    # arredondando o numero de casa decimais para 2
    data.round(decimals=4)
    
    return data

def edf_extract_features(features,start_time, end_time):
    """ Cleanses the EDF data by selecting the relevant time interval and extracting wavelet coefficients."""

    start_time_seconds = to_seconds(start_time)
    end_time_seconds = to_seconds(end_time)

    features.index = features.time
    features = features.drop(['time'], axis=1)

    features = features[start_time_seconds:end_time_seconds]

    coeffs = pywt.wavedec(features, 'coif1', level=5)
    cA5, cD5, cD4, cD3, cD2, cD1 = coeffs

    vetor_coif = np.array([
                cA5.mean(), cD5.mean(), cD4.mean(), cD3.mean(), cD2.mean(), cD1.mean(),
                np.std(cA5), np.std(cD5), np.std(cD4), np.std(
                    cD3), np.std(cD2), np.std(cD1),
                cA5.max(), cD5.max(), cD4.max(), cD3.max(), cD2.max(), cD1.max(),
                cA5.min(), cD5.min(), cD4.min(), cD3.min(), cD2.min(), cD1.min()
            ])
    
    vetor_coif = np.atleast_2d(vetor_coif)
    vetor_coif = pd.DataFrame(vetor_coif, columns=feature_columns)

    return vetor_coif

def process_edf(file, start_time, end_time):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

    raw_features = read_edf(tmp_path)
    processed_features = edf_extract_features(raw_features, start_time, end_time)

    return processed_features


