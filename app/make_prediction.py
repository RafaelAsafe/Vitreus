import pickle
from config import config
import pandas as pd

TEST_EXAM_FILENAME = config.get('locations','test_exam_filename')
PICKLE_MODULE_FILENAME = config.get('locations','pickle_location')

# making predictions with the saved model

dataset_test = pd.read_excel(test_exam_filename)

loaded_model = pickle.load(open(PICKLE_MODULE_FILENAME, 'rb'))

prediction = loaded_model.predict((dataset_test.drop(['cod_exame','id_paciente','diagnostico'],axis=1)))
print(prediction)
