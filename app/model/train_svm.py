###############
# 1. Imports  #
###############
import pickle
import numpy as np
import pandas as pd
from sklearn import svm
from decouple import config
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix


################
# 2 . Funções  #
################

def mean_norm(df_input):
    return df_input.apply(lambda x: (x - x.mean()) / x.std(), axis=0)

###################
# 3. config setup #
###################


DATASET_FILENAME = config('DATASET_FILENAME')
PICKLE_LOCATION = config('pickle_location')


############################
# 4. Variaveis estáticas   #
############################

##########
# 4. ETL #
########## 

dataset = pd.read_excel(DATASET_FILENAME)

y = dataset['diagnostico_bin']
# x = dataset.drop(['diagnostico', 'diagnostico_bin',
#                  'cod_exame', 'id_paciente','Unnamed: 0'], axis=1)
x = dataset[['mediaA5','mediaD5','mediaD1','mediaD2','mediaD3','mediaD4']]
 

for i in range(10):
    
    balanceamento = {1: 1, 0: 2}
    model = svm.SVC(kernel='rbf', class_weight=balanceamento)
    model.fit(x, y)
    kfold = KFold(n_splits=5, shuffle=True)
    result = cross_val_score(model, x, y, cv=kfold,scoring='accuracy')

    # conf_mat = confusion_matrix(y, y_pred)

    # print("K-Fold RECALL Scores: {0}".format(result))
    # print("RECALL for Cross-Validation K-Fold: {0}".format(result.mean()))

    # print("K-Fold average_precision Scores: {0}".format(result))
    # print("average_precision for Cross-Validation K-Fold: {0}".format(result.mean()))

    print("K-Fold accuracy Scores: {0}".format(result))
    print("accuracy for Cross-Validation K-Fold: {0}".format(result.mean()))
 


# save
with open(PICKLE_LOCATION, 'wb') as f:
    pickle.dump(model, f)
