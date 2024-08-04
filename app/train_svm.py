###############
# 1. Imports  #
###############
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn import svm
import pandas as pd
import pickle

################
# 2 . Funções  #
################


def mean_norm(df_input):
    return df_input.apply(lambda x: (x - x.mean()) / x.std(), axis=0)

###################
# 3. config setup #
###################

############################
# 4. Variaveis estáticas   #
############################

##########
# 4. ETL #
##########

dataset = pd.read_excel(config.get('dataset_filename'))
dataset.set_index('id_paciente', inplace=True)
dataset_normalizado_x = mean_norm(
    dataset.drop(['cod_exame', 'diagnostico'], axis=1))
dataset_normalizado_x.plot(kind='bar')
dataset['diagnostico_bin'] = np.where(dataset['diagnostico'] == 'PNES', 1, 0)
x = dataset.drop(['diagnostico', 'diagnostico_bin', 'cod_exame'], axis=1)
x_norm = dataset_normalizado_x
y = dataset['diagnostico_bin']

balanceamento = {1: 1.8, 0: 1}
model = svm.SVC(kernel='linear', class_weight=balanceamento)

kfold = KFold(n_splits=4, shuffle=True)
result = cross_val_score(model, x, y, cv=kfold)

print("K-Fold (R^2) Scores: {0}".format(result))
print("Mean R^2 for Cross-Validation K-Fold: {0}".format(result.mean()))

# save
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
