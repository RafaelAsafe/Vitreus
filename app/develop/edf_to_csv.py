import os
import mne
import pandas as pd
import datetime
from decouple import config

from src.constants import anodo_eeg_1, catodo_eeg_1, channels_names_1, anodo_eeg_2, catodo_eeg_2, channels_names_2
from src.utils import to_seconds


ORIGIN_DIRECTORY = config('RAW_EXAMS_DIRETORY')
DESTINY_DIRECTORY = config('PROCESSING_EXAMS_DIRECTORY')

horario = str(datetime.time()).replace(':', '-')

if not os.path.exists('./data/exams/processed/PNES'):
    os.makedirs('./data/exams/processed/PNES')
    os.makedirs('./data/exams/processed/SE')

for diretorio, subpastas, arquivos in os.walk(ORIGIN_DIRECTORY):
    for arquivo in arquivos:
        try:   
            print(f'------------------{arquivo}-------------------')
        
            path = os.path.join(diretorio, arquivo)
            raw_data = mne.io.read_raw_edf(path, preload=True, encoding='latin1').load_data()

            try:
                raw_bip_ref = mne.set_bipolar_reference(raw_data, anodo_eeg_1, catodo_eeg_1, channels_names_1, verbose=False)
                raw_bip_ref.pick_channels(channels_names_1, verbose=False)
            except ValueError:
                raw_bip_ref = mne.set_bipolar_reference(raw_data, anodo_eeg_2, catodo_eeg_2, channels_names_2, verbose=False)
                raw_bip_ref.pick_channels(channels_names_2, verbose=False)


            tempo_inicio_exame = to_seconds(raw_bip_ref.info.get('meas_date').time())
            
            data = raw_bip_ref.to_data_frame()
            
            #adicionando referencial de tempo
            data['time'] = data['time'] + tempo_inicio_exame
            
            # arredondando o numero de casa decimais para 2
            data.round(decimals=4)

            remove_extesion = arquivo.split('.')
            arquivo = remove_extesion[0]

            if 'PNES' in diretorio:
                destiny_path = os.path.join(
                    DESTINY_DIRECTORY+'PNES/', arquivo)
            else:
                destiny_path = os.path.join(DESTINY_DIRECTORY+'SE/', arquivo)

            data.to_excel(destiny_path + '.xlsx', index=False)

        except Exception as e:
            print(f"arquivo:{arquivo} apresentou o erro \n \n \n \n{e}")
            with open(f'log_text_{horario}.csv', 'a') as f:
                f.write(f'{arquivo}#{e}\n')
