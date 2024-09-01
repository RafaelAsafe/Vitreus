import pickle
from config import config
import pandas as pd

test_exam_filename = config.get('locations','test_exam_filename')
pickle_module_filename = config.get('locations','pickle_location')

# making predictions with the saved model

dataset_test = pd.read_excel(test_exam_filename)

loaded_model = pickle.load(open(pickle_module_filename, 'rb'))

prediction = loaded_model.predict((dataset_test.drop(['cod_exame','id_paciente','diagnostico'],axis=1)))
print(prediction)
