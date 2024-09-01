import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pywt import wavedec
import seaborn as sns
import os
import re
from config import config

diretorio_raiz = config.get('locations','diretorio_exames')
diretorio_SE = config.get('locations','diretorio_exames_se')
diretorio_PNES = config.get('locations','diretorio_exames_pnes')
diretorio_destino = config.get('locations','diretorio_dataset')

atributos = ['id_paciente', 'cod_exame', 'mediaA5', 'mediaD5', 'mediaD4', 'mediaD3', 'mediaD2', 'mediaD1', 'desvpadA5',
             'desvpadD5', 'desvpadD4', 'desvpadD3', 'desvpadD2', 'desvpadD1', 'maximoA5',
             'maximoD5', 'maximoD4', 'maximoD3', 'maximoD2', 'maximoD1', 'minimoA5',
             'minimoD5', 'minimoD4', 'minimoD3', 'minimoD2', 'minimoD1', 'diagnostico']

dataset = pd.DataFrame(data=None, columns=atributos)


for diretorio, subpastas, arquivos in os.walk(diretorio_raiz):
    for file_name in arquivos:

        print(file_name)
        patient_event = pd.read_excel(os.path.join(diretorio, file_name))
        patient_event.index = patient_event.time
        patient_event = patient_event.drop(['time'], axis=1)

        amostragem = len(patient_event)/200
        comprimento_sinal = int(amostragem)
        discrete_patient_event = patient_event.iloc[::comprimento_sinal, :]

        coeffs = wavedec(patient_event, 'coif1', level=5)
        cA5, cD5, cD4, cD3, cD2, cD1 = coeffs

        vc_coif = np.array([
            cA5.mean(), cD5.mean(), cD4.mean(), cD3.mean(), cD2.mean(), cD1.mean(),
            np.std(cA5), np.std(cD5), np.std(cD4), np.std(
                cD3), np.std(cD2), np.std(cD1),
            cA5.max(), cD5.max(), cD4.max(), cD3.max(), cD2.max(), cD1.max(),
            cA5.min(), cD5.min(), cD4.min(), cD3.min(), cD2.min(), cD1.min()
        ])

        m = re.search(r"(?<=Patient)(.*?)(?=-)", file_name)
        patientid = m.group(0)

        n = re.search(r"(?<=-).*", file_name)
        code_exam = n.group(0)

        if diretorio == diretorio_PNES:
            diagnostico = 'PNES'
        elif diretorio == diretorio_SE:
            diagnostico = 'SE'
        else:
            diagnostico = 'error'

        dados = [patientid, code_exam]
        dados = [y for x in [dados, vc_coif] for y in x]
        dados.append(diagnostico)

        dados_row = np.atleast_2d(dados)
        df_row = pd.DataFrame(dados_row, columns=atributos)
        dataset = pd.concat([dataset, df_row], ignore_index=True)


dataset.to_excel(os.path.join(diretorio_destino,'dataset_raw.xlsx'))

dataset['diagnostico_bin'] = np.where(dataset['diagnostico'] == 'PNES', 1, 0)
dataset.drop(columns=['code_exam','patientid'])

dataset.to_excel(os.path.join(diretorio_destino,'dataset.xlsx'))

dataset_normalizado_x = mean_norm(dataset)

dataset.to_excel(os.path.join(diretorio_destino,'dataset_normalizado.xlsx'))