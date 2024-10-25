import os
import pickle
import pandas as pd
from config import config

# TEST_EXAM_FILENAME = config.get('locations', 'test_exam_filename')
# PICKLE_MODULE_FILENAME = config.get('locations', 'pickle_location')

# making predictions with the saved model
PICKLE_MODULE_FILENAME = 'E:\GIT\Vitreus\data\model.pkl'

print(os.getcwd())

def make_infer(dataset):
    
    dataset_test = pd.read_excel(dataset)

    loaded_model = pickle.load(open(PICKLE_MODULE_FILENAME, 'rb'))

    prediction = loaded_model.predict(
        (dataset_test.drop(['cod_exame', 'id_paciente', 'diagnostico'], axis=1)))
    return prediction


# print(make_infer(TEST_EXAM_FILENAME, PICKLE_MODULE_FILENAME))
