import streamlit as st
import pandas as pd
from datetime import datetime
from model.make_prediction import make_infer
from decouple import config
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
# from utils import edf_handler

DATASET_FILENAME = config('DATASET_FILENAME')

st.title("Teste seu modelo!")

st.write("envie seu arquivo picke!")


if 'button' not in st.session_state:
    st.session_state['button'] = False


def click_button():
    st.session_state['button'] = not st.session_state['button']


st.button("Pickle do Modelo", on_click=click_button)


if st.session_state['button']:
    uploaded_file = st.file_uploader("Choose a file")
    st.session_state.clicked = False

    if uploaded_file is not None:
        try:
            # df_exam = edf_handler(uploaded_file)
            loaded_model = pickle.load(uploaded_file)
            dataset = pd.read_excel(DATASET_FILENAME)
            y = dataset['diagnostico_bin']
    #       x = dataset.drop(['diagnostico', 'diagnostico_bin',
    #                  'cod_exame', 'id_paciente','Unnamed: 0'], axis=1)
            x = dataset[['mediaA5','mediaD5','mediaD1','mediaD2','mediaD3','mediaD4']]
            result = cross_val_score(loaded_model, x, y, cv=kfold)
            print(result)

        except Exception as e:
            st.error(f"Erro ao ler o arquivo {e}")