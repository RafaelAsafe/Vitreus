import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pywt
from decouple import config
from intervalos_exames import intervalos_exames

def to_seconds_list(list_tempo):
    return (list_tempo[0] * 3600 + list_tempo[1] * 60 +  list_tempo[2])

PROCESSING_EXAMS_DIRECTORY = config('PROCESSING_EXAMS_DIRECTORY')
DIRETORIO_SE_PROCESSADOS = config('DIRETORIO_SE_PROCESSADOS')
DIRETORIO_PNES_PROCESSADOS = config('DIRETORIO_PNES_PROCESSADOS')
DATASET_DESTINY = config('DATASET_DESTINY')

atributos = ['id_paciente', 'cod_exame', 'mediaA5', 'mediaD5', 'mediaD4', 'mediaD3', 'mediaD2', 'mediaD1', 'desvpadA5',
             'desvpadD5', 'desvpadD4', 'desvpadD3', 'desvpadD2', 'desvpadD1', 'maximoA5',
             'maximoD5', 'maximoD4', 'maximoD3', 'maximoD2', 'maximoD1', 'minimoA5',
             'minimoD5', 'minimoD4', 'minimoD3', 'minimoD2', 'minimoD1', 'diagnostico']

dataset = pd.DataFrame(data=None, columns=atributos)


for diretorio, subpastas, arquivos in os.walk(PROCESSING_EXAMS_DIRECTORY):
    for file_name in arquivos:
        try:
            print(file_name)

            patient_event = pd.read_excel(os.path.join(diretorio, file_name))

            inicio_evento, final_evento = intervalos_exames[file_name]

            inicio_evento_seconds = to_seconds_list(inicio_evento)
            final_evento_seconds = to_seconds_list(final_evento)            
            
            
            patient_event.index = patient_event.time
            patient_event = patient_event.drop(['time'], axis=1)

            patient_event = patient_event[inicio_evento_seconds:final_evento_seconds]

            # puxando os intervalos de 1 segundo - remover para criar um dataset com os dados inteiros
            # amostragem = len(patient_event)/200
            # comprimento_sinal = int(amostragem)
            # discrete_patient_event = patient_event.iloc[::comprimento_sinal, :]

            coeffs = pywt.wavedec(patient_event, 'coif1', level=5)
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

            if diretorio == DIRETORIO_PNES_PROCESSADOS:
                diagnostico = 'PNES'
            elif diretorio == DIRETORIO_SE_PROCESSADOS:
                diagnostico = 'SE'
            else:
                diagnostico = 'error'

            dados = [patientid, code_exam]
            dados = [y for x in [dados, vc_coif] for y in x]
            dados.append(diagnostico)

            dados_row = np.atleast_2d(dados)
            df_row = pd.DataFrame(dados_row, columns=atributos)
            dataset = pd.concat([dataset, df_row], ignore_index=True)
        except Exception as e:
            print(f'erro: {e}')

dataset.to_excel(os.path.join(DATASET_DESTINY, 'dataset_raw_teste2.xlsx'))

dataset['diagnostico_bin'] = np.where(dataset['diagnostico'] == 'PNES', 1, 0)
dataset.drop(columns=['cod_exame', 'id_paciente'])

dataset.to_excel(os.path.join(DATASET_DESTINY, 'dataset_1sec_teste2.xlsx'))

# dataset_normalizado_x = mean_norm(dataset)

# dataset.to_excel(os.path.join(DATASET_DESTINY,
#                  'dataset_1sec_normalizado_teste.xlsx'))
