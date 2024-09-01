###############
# 1. Imports  #
###############
import pickle
import numpy as np
import pandas as pd
from sklearn import svm
from config import config
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold


################
# 2 . Funções  #
################

def mean_norm(df_input):
    return df_input.apply(lambda x: (x - x.mean()) / x.std(), axis=0)

###################
# 3. config setup #
###################

DATASET_FILENAME = config.get('locations', 'dataset_filename')
PICKLE_LOCATION = config.get('locations', 'pickle_location')

############################
# 4. Variaveis estáticas   #
############################

##########
# 4. ETL #
##########

dataset = pd.read_excel(DATASET_FILENAME)

x = dataset.drop(['diagnostico', 'diagnostico_bin', 'cod_exame'], axis=1)
y = dataset['diagnostico_bin']
balanceamento = {1: 1.8, 0: 1}
model = svm.SVC(kernel='linear', class_weight=balanceamento)
model.fit(x,y)
kfold = KFold(n_splits=4, shuffle=True)
result = cross_val_score(model, x, y, cv=kfold)

print("K-Fold (R^2) Scores: {0}".format(result))
print("Mean R^2 for Cross-Validation K-Fold: {0}".format(result.mean()))

# save
with open(PICKLE_LOCATION, 'wb') as f:
    pickle.dump(model, f)
