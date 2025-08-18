###############
# 1. Imports  #
###############
import pickle
import pandas as pd
from sklearn import svm
from decouple import config
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn import preprocessing
import numpy as np


################
# 2 . Funções  #
################

def mean_norm(df_input):
    return df_input.apply(lambda x: (x - x.mean()) / x.std(), axis=0)

###################
# 3. config setup #
###################


DATASET_FILENAME = config('DATASET_FILENAME')
PICKLE_LOCATION = config('PICKLE_LOCATION')


############################
# 4. Variaveis estáticas   #
############################

##########
# 4. ETL #
########## 
print(DATASET_FILENAME)
dataset = pd.read_excel(DATASET_FILENAME)


y = dataset['diagnostico_bin']

# x = dataset.drop(['diagnostico', 'diagnostico_bin',
#                  'cod_exame', 'id_paciente'], axis=1)

x = preprocessing.normalize(dataset[['mediaD2', 'desvpadD1', 'maximoA5', 'maximoD5', 'maximoD1']],axis=0)
x_raw = dataset[['mediaD2', 'desvpadD1', 'maximoA5', 'maximoD5', 'maximoD1']]
norms = np.linalg.norm(x_raw, axis=0)


# x= preprocessing.normalize(dataset[['maximoA5', 'maximoD5', 'minimoD4', 'minimoD3', 'minimoD2']],axis=0)
# x = preprocessing.normalize(dataset.drop(['diagnostico', 'diagnostico_bin','cod_exame', 'id_paciente'], axis=1),axis=0)

for j in ['accuracy','recall','average_precision','roc_auc']:
    for i in range(10):
        
        balanceamento = {1: 2, 0: 1}
        gamma = 3.59381
        parametro_regulador = 1000
        
        # 'poly', 'sigmoid', 'rbf', 'linear'
        model = svm.SVC(kernel='rbf', class_weight=balanceamento,gamma=gamma,C=parametro_regulador,cache_size=2000)
        model.fit(x, y)
        kfold = KFold(n_splits=5, shuffle=True)
        result = cross_val_score(model, x, y, cv=kfold,scoring=j)


        # print(f"K-Fold {j} Scores: {result}\n")
        # print(f"{j} for Cross-Validation K-Fold: {result.mean()}\n")
        # print("\n---------------------x-----------------\n") 
print(f'Predict y PNES:{model.predict(x)[:36]}\n\nPredict total y:{model.predict(x)}')


# save
with open(PICKLE_LOCATION, 'wb') as f:
    pickle.dump(model, f)
