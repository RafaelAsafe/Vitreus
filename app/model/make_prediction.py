import os
import pickle
from decouple import config

from src.mne_handler import process_edf
from src.constants import norms

# TEST_EXAM_FILENAME = config('test_exam_filename')
PICKLE_MODULE_FILENAME = config('PICKLE_LOCATION')


print(os.getcwd())


def make_infer(exam, ictal_start, ictal_end):

    features = process_edf(exam, ictal_start, ictal_end)

    optimized_features = features[['mediaD2', 'desvpadD1', 'maximoA5', 'maximoD5', 'maximoD1']].values / norms

    loaded_model = pickle.load(open(PICKLE_MODULE_FILENAME, 'rb'))

    prediction = loaded_model.predict(optimized_features)
    
    return prediction[0]
