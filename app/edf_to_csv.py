import os
import mne
import pandas as pd
import datetime
from config import config

ORIGIN_DIRECTORY = config.get('locations','raw_exams_diretory')
DESTINY_DIRECTORY = config.get('locations','processing_exams_directory')

horario = str(datetime.time()).replace(':', '-')

if not os.path.exists('./data/exams/processed/PNES'):
    os.mkdir('./data/exams/processed/PNES')
    os.mkdir('./data/exams/processed/SE')

for diretorio, subpastas, arquivos in os.walk(ORIGIN_DIRECTORY):
    for arquivo in arquivos:
        print(f'------------------{arquivo}-------------------')
        try:
            path = os.path.join(diretorio, arquivo)
            raw_data = mne.io.read_raw_edf(
                path, preload=True, encoding='latin1').load_data()

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

            raw_bip_ref = mne.set_bipolar_reference(
                raw_data, anodo_eeg_1, catodo_eeg_1, channels_names_1, verbose=False)
            raw_bip_ref.pick_channels(channels_names_1, verbose=False)

            low_freq, high_freq = 0.3, 35.0
            raw_bip_ref = raw_bip_ref.filter(
                low_freq, high_freq, n_jobs=4, verbose=False)

            data = raw_bip_ref.to_data_frame()
            # arredondando o numero de casa decimais para 2
            data.round(decimals=2)

            remove_extesion = arquivo.split('.')
            arquivo = remove_extesion[0]
            
            if 'PNES' in diretorio:
                destiny_path = os.path.join(DESTINY_DIRECTORY+'/PNES/', arquivo)
            else:
                destiny_path = os.path.join(DESTINY_DIRECTORY+'/SE/', arquivo)


            data.to_excel(destiny_path + '.xlsx', index=False)
            
        except ValueError:
            path = os.path.join(diretorio, arquivo)
            raw_data = mne.io.read_raw_edf(
                path, preload=True, encoding='latin1').load_data()
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

            raw_bip_ref = mne.set_bipolar_reference(
                raw_data, anodo_eeg_2, catodo_eeg_2, channels_names_2, verbose=False)

            raw_bip_ref.pick_channels(channels_names_2, verbose=False)

            low_freq, high_freq = 0.3, 35.0
            raw_bip_ref = raw_bip_ref.filter(
                low_freq, high_freq, n_jobs=4, verbose=False)

            data = raw_bip_ref.to_data_frame()
            # arredondando o numero de casa decimais para 2
            data.round(decimals=2)

            remove_extesion = arquivo.split('.')
            arquivo = remove_extesion[0]

            if 'PNES' in diretorio:
                destiny_path = os.path.join(DESTINY_DIRECTORY+'/PNES/', arquivo)
            else:
                destiny_path = os.path.join(DESTINY_DIRECTORY+'/SE/', arquivo)

            data.to_excel(destiny_path + '.xlsx', index=False)

        except Exception as e:
            print(f"arquivo:{arquivo} apresentou o erro \n \n \n \n{e}")
            with open(f'log_text_{horario}.csv', 'a') as f:
                f.write(f'{arquivo}#{e}\n')
