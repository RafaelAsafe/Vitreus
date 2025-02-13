import os
import mne
import pandas as pd
import datetime
from decouple import config

def to_seconds(datetime_time):
    return (datetime_time.hour * 3600 + datetime_time.minute * 60 +  datetime_time.second)

ORIGIN_DIRECTORY = config('RAW_EXAMS_DIRETORY')
DESTINY_DIRECTORY = config('PROCESSING_EXAMS_DIRECTORY')

horario = str(datetime.time()).replace(':', '-')

anodo_eeg_1 = ['EEG Fp1-Ref',  'EEG F3-Ref',  'EEG C3-Ref',  'EEG P3-Ref',  'EEG Fp1-Ref',  'EEG F7-Ref',  'EEG T7-Ref',  'EEG P7-Ref',  'EEG Fp2-Ref',
                    'EEG F4-Ref',  'EEG C4-Ref',  'EEG P4-Ref', 'EEG Fp2-Ref',  'EEG F8-Ref',  'EEG T8-Ref',  'EEG P8-Ref',  'EEG Fz-Ref',  'EEG Cz-Ref']

catodo_eeg_1 = ['EEG F3-Ref', 'EEG C3-Ref', 'EEG P3-Ref', 'EEG O1-Ref', 'EEG F7-Ref', 'EEG T7-Ref', 'EEG P7-Ref', 'EEG O1-Ref', 'EEG F4-Ref',
                'EEG C4-Ref', 'EEG P4-Ref', 'EEG O2-Ref', 'EEG F8-Ref', 'EEG T8-Ref', 'EEG P8-Ref', 'EEG O2-Ref', 'EEG Cz-Ref', 'EEG Pz-Ref']

channels_names_1 = ['Fp1-F3',
                    'F3-C3',
                    'C3-P3',
                    'P3-O1',
                    'Fp1-F7',
                    'F7-T7',
                    'T7-P7',
                    'P7-O1',
                    'Fp2-F4',
                    'F4-C4',
                    'C4-P4',
                    'P4-O2',
                    'Fp2-F8',
                    'F8-T8',
                    'T8-P8',
                    'P8-O2',
                    'Fz-Cz',
                    'Cz-Pz']

anodo_eeg_2 = ['EEG Fp1-Ref', 'EEG F3-Ref', 'EEG C3-Ref', 'EEG P3-Ref', 'EEG Fp1-Ref', 'EEG F7-Ref', 'EEG T3-Ref', 'EEG T5-Ref',
                           'EEG Fp2-Ref', 'EEG F4-Ref', 'EEG C4-Ref', 'EEG P4-Ref', 'EEG Fp2-Ref', 'EEG F8-Ref', 'EEG T4-Ref', 'EEG T6-Ref', 'EEG Fz-Ref', 'EEG Cz-Ref']

catodo_eeg_2 = ['EEG F3-Ref', 'EEG C3-Ref', 'EEG P3-Ref', 'EEG O1-Ref', 'EEG F7-Ref', 'EEG T3-Ref', 'EEG T5-Ref', 'EEG O1-Ref', 'EEG F4-Ref',
                'EEG C4-Ref', 'EEG P4-Ref', 'EEG O2-Ref', 'EEG F8-Ref', 'EEG T4-Ref', 'EEG T6-Ref', 'EEG O2-Ref', 'EEG Cz-Ref', 'EEG Pz-Ref']

channels_names_2 = ['Fp1-F3',
                    'F3-C3',
                    'C3-P3',
                    'P3-O1',
                    'Fp1-F7',
                    'F7-T3',
                    'T3-T5',
                    'T5-O1',
                    'Fp2-F4',
                    'F4-C4',
                    'C4-P4',
                    'P4-O2',
                    'Fp2-F8',
                    'F8-T4',
                    'T4-T6',
                    'T6-O2',
                    'Fz-Cz',
                    'Cz-Pz']


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
            data['time']= data['time'] + tempo_inicio_exame
            
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
